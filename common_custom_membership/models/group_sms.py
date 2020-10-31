from odoo import models, api, fields,_
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import time
from odoo.exceptions import UserError, ValidationError
import math, random
import requests
from odoo.exceptions import ValidationError


class SendCourseSMS(models.Model):
    _name = 'op.sms.line'
    _rec_name = 'member_id'

    member_id = fields.Many2one('op.member', string='Members', required=True)
    mobile = fields.Char('mobile')
    phone = fields.Char('Phone')
    sms_id = fields.Many2one('op.sms', string='Sms', required=False, invisible=True)


class SendSMS(models.Model):
    _name = 'op.sms'
    _rec_name = 'district_id'

    district_id = fields.Many2one('op.district', string='District', required=True)
    union_id = fields.Many2one('op.union', string='Union', required=False)
    panchayat_id = fields.Many2one('op.panchayat', string='Panchayat', required=False)
    message = fields.Text(string="Message", required=True)
    sms_line_ids = fields.One2many(
        'op.sms.line', 'sms_id', 'Members info')

    @api.onchange('district_id')
    def onchange_disrict_id(self):
        self.union_id =False
        self.panchayat_id =False

    @api.onchange('union_id')
    def onchange_union_id(self):
        self.panchayat_id =False

    @api.multi
    @api.onchange('district_id','union_id', 'panchayat_id')
    def onchange_category_id(self):
        '''Method to get standard of student selected'''
        for rec in self:
            if rec.panchayat_id and rec.union_id and rec.district_id:
                rec.onchange_panchayat()
            if not rec.panchayat_id and rec.union_id and rec.district_id:
                rec.onchange_union()
            if not rec.panchayat_id and not rec.union_id and rec.district_id:
                rec.onchange_member_id()

    @api.multi
    def onchange_panchayat(self):
        stud_obj = self.env['op.member']
        student_list = []
        for rec in self:
            if rec.district_id and rec.union_id and rec.panchayat_id:
                member_ids = stud_obj.search([('district_id', '=', rec.district_id.id),('union_id', '=', rec.union_id.id),
                                              ('panchayat_id', '=', rec.panchayat_id.id)])
                for stud in member_ids:
                    student_list.append({'member_id': stud.id,
                                         'mobile': stud.mobile,
                                         'phone':stud.phone
                                         })
            logging.info('panchayat')
            logging.info(student_list)
            rec.sms_line_ids = False
            rec.sms_line_ids=student_list

    @api.multi
    def onchange_union(self):
        stud_obj = self.env['op.member']
        student_list = []
        for rec in self:
            if rec.district_id and rec.union_id and not rec.panchayat_id:
                member_ids = stud_obj.search([('district_id', '=', rec.district_id.id),('union_id', '=', rec.union_id.id)])
                for stud in member_ids:
                    student_list.append({'member_id': stud.id,
                                         'mobile': stud.mobile,
                                         'phone':stud.phone
                                         })
            logging.info('union')
            logging.info(student_list)
            rec.sms_line_ids = False
            rec.sms_line_ids = student_list
            if rec.panchayat_id:
                rec.onchange_panchayat()

    @api.multi
    def onchange_member_id(self):
        '''Method to get course and batch of student selected'''
        stud_obj = self.env['op.member']
        student_list = []
        for rec in self:
            if rec.district_id and not rec.union_id and not rec.panchayat_id:
                logging.info(rec.district_id)
                member_ids = stud_obj.search([('district_id', '=', rec.district_id.id)])
                logging.info(member_ids)
                for stud in member_ids:
                    student_list.append({'member_id': stud.id,
                                         'mobile': stud.mobile,
                                         'phone':stud.phone
                                         })
                    logging.info(student_list)
            rec.sms_line_ids = False
            rec.sms_line_ids = student_list
            if rec.union_id:
                rec.onchange_union()

    def send_message(self):
        for rec in self:
            logging.info(len(rec.message))
            if len(rec.message) > 115:
                raise ValidationError(_("Reduce the message length to be within 55 characters when using Tamil Font "
                                        "and 115 when using Engligh font."))
            member = rec.sms_line_ids
            num_test = ''
            sms_count = 0
            for mem in member:
                student = mem.member_id
                number = student.mobile
                logging.info(student)
                logging.info(number)
                if student.mobile:
                    sms_count = sms_count + 1
                    logging.info('sms_count')
                    logging.info(sms_count)
                if student.phone:
                    phone = student.phone
                    logging.info(phone)
                #     self.env['sms.api']._send_sms(phone, self.message)
                # self.env['sms.api']._send_sms(number, self.message)
                if student.mobile != False:
                    if num_test == '':
                        num_test += str(student.mobile)
                    else:
                        num_test += ','
                        num_test += str(student.mobile)
                if student.phone != False:
                    if num_test == '':
                        num_test += str(student.phone)
                    else:
                        num_test += ','
                        num_test += str(student.phone)
                logging.info(num_test)
            li = num_test
            numbers = li.split(',')
            logging.info(numbers)
            for num in numbers:
                logging.info(num)
                myUrl = 'https://app.theuolo.com/notes/send'
                head = {'Content-Type': 'application/x-www-form-urlencoded',
                        'Authorization': 'MTcwMjo6VW5pcXVlSWRmb3JOb3Rlc1NlcnZpY2U='}
                logging.info(head)
                message = self.message
                # type = '2'
                type = '1'
                part_1 = "\"-1\""
                receiver_user_ids = '{'+part_1 +':'+ '"'+num+'"''}'
                logging.info(receiver_user_ids)
                digits = "0123456789"
                request_number = ""
                for i in range(3):
                    request_number += digits[math.floor(random.random() * 10)]
                request_id = request_number
                logging.info(request_id)
                form_data = {
                    # 'receivergroupids': 'AULZN',
                    'receiveruserids':receiver_user_ids,
                    'requestid': request_id,
                    'message': message,
                    'type': type
                }
                logging.info(form_data)
                response = requests.request('POST', url=myUrl, data=form_data, headers=head)
                logging.info(response)
                logging.info(response.text)

            # company_name = self.env.user.company_id.name
            # return {
            #     'name': 'SMS',
            #     'type': 'ir.actions.act_url',
            #     'url': "http://173.45.76.227/send.aspx?username=Annaitherasa&pass=GeorgeIndia@123&route=trans1&senderid=AnnaiN&numbers=" + num_test + "&message=" + self.message,
            #     'target': 'new',
            #     'res_id': self.id,
            # }

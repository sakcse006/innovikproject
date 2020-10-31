from odoo import models, api, fields,_
import logging,requests,json
import re
from odoo.exceptions import ValidationError


class OpRegistrationWizard(models.Model):
    _name = 'op.registration.wizard'

    party_name = fields.Char(string="Party Name", required=True)
    admin_name = fields.Char(string="Admin Name", required=True)
    admin_login_email_id = fields.Char(string="Email", required=True)
    login_password = fields.Char(string="Password", required=True)
    admin_contact_number = fields.Char(string=" Admin Contact name", required=True)
    phone_number = fields.Char(string="Phone Number", required=True)
    progress_rate = fields.Integer(string='Sample Rate',default="0",invisable=False)
    maximum_rate = fields.Integer(string='Maximum Rate',default="100",invisable=False)
    # sales = fields.Boolean('Sales,Purchase and Inventory')
    # fees = fields.Boolean('Fees')
    # timetable = fields.Boolean('Timetable')
    # nursery_school = fields.Boolean('Nursery School')
    # primary_school = fields.Boolean('Primary School')
    # high_school = fields.Boolean('High School')
    # hr_sec_school = fields.Boolean('Higher Secondary School')

    @api.onchange('admin_login_email_id')
    def validate_mail(self):
        if self.admin_login_email_id:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.admin_login_email_id)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')
            else:
                email = self.env['op.registration.wizard'].search([('admin_login_email_id', '=', self.admin_login_email_id)])
                if email:
                    raise ValidationError(_('Email is Already Exist!'))

    def submit(self):
        logging.info(self.party_name)
        # logging.info(self.sales)
        db_name = self.party_name
        admin_name = self.admin_name
        admin_login_email_id = self.admin_login_email_id
        login_password = self.login_password
        admin_contact_number = self.admin_contact_number
        phone_number = self.phone_number
        # app_names = []
        # school_type = []
        # if self.sales:
        #     sales = 'sales'
        #     app_names.append(sales)
        # if self.fees:
        #     fees = 'fees'
        #     app_names.append(fees)
        # if self.nursery_school:
        #     nursery_school = 'Nursery School'
        #     school_type.append(nursery_school)
        # if self.primary_school:
        #     primary_school = 'Primary School'
        #     school_type.append(primary_school)
        # if self.high_school:
        #     high_school = 'High School'
        #     school_type.append(high_school)
        # if self.hr_sec_school:
        #     hr_sec_school = 'Hr.Sec.School'
        #     school_type.append(hr_sec_school)

        data = {
            'db_name': db_name,
            'school_name': admin_name,
            'db_username': admin_login_email_id,
            'db_password': login_password,
            'contact_person_name':admin_contact_number,
            'phone_number':phone_number,
            'app_names':[],
            'school_type':[]
        }
        logging.info(data)
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            url = "http://localhost:8000/create_school_db"
            # url = "http://locathost:5011/create_school_db"
            response = requests.post(url=url,headers=headers, data=json.dumps(data))
            logging.info(response)
            # if response.status_code == 200:
            result = response.json()
            register_result = result['message']
            
            logging.info(register_result)
            return {
                    'name': 'Message',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'custom.pop.message',
                    'target':'new',
                    'context':{'default_name': register_result}
                    }

        except Exception:
            register_result = "due to exception, Server is not running. Please contact system administrator!"
            logging.info(register_result)
            return {
                    'name': 'Message',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'custom.pop.message',
                    'target':'new',
                    'context':{'default_name': register_result}
                    }


class CustomPopMessage(models.TransientModel):
    _name = "custom.pop.message"

    name = fields.Char('Message')

    def reload(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

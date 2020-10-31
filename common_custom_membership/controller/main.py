from odoo import http
from odoo.http import request
import logging,requests,json


class RegistrationForm(http.Controller):
    @http.route('/party-registration',website=True,type="http",auth="public",csrf=False)
    def registration_form(self):
        return request.render('common_custom_membership.view_party_registration_form',{})

    @http.route('/party_registration_form_submit',website=True,type="http",auth="public",csrf=False)
    def submit_website(self,**post):
        db_names = post.get('party_name')
        db_name=db_names.replace(" ", "_")
        admin_name = post.get('admin_name')
        db_username = post.get('admin_login_email_id')
        db_password = post.get('login_password')
        admin_contact_number = post.get('admin_contact_number')
        phone_number = post.get('phone_number')

        vals = {'party_name': db_name,
                'admin_name':admin_name,
                'admin_login_email_id':db_username,
                'login_password':db_password,
                'admin_contact_number':admin_contact_number,
                'phone_number':phone_number
                }
        logging.info(vals)
        check_email = request.env['op.registration.wizard'].sudo().search([('admin_login_email_id','=',db_username)], limit=1)
        if check_email.id:
            register_result = 'Email Id already Exists!'
            return request.render('common_custom_membership.registration_result', {'result':register_result})
        # request.env['op.registration.wizard'].sudo().create(vals)

        data = {
            'db_name': db_name,
            'db_username': db_username,
            'db_password': db_password,
        }
        logging.info(data)
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            # url = "http://3.23.14.196:5011/create_school_db"
            url = "http://localhost:8000/create_school_db"
            logging.info(url)

            response = requests.post(url=url,headers=headers, data=json.dumps(data))
            logging.info(response)
            logging.info(response.json())
            if response.status_code == 500:
                result = response.json()
                register_result = result['message']
                return request.render('common_custom_membership.registration_result', {'result': register_result})
            result = response.json()
            register_result = result['message']
            logging.info(register_result)
            request.env['op.registration.wizard'].sudo().create(vals)
            return request.render('common_custom_membership.registration_result',{'result':register_result})

        except Exception:
            register_result = "Server is not running. Please contact system administrator!"
            logging.info(register_result)
            return request.render('common_custom_membership.registration_result',{'result':register_result})


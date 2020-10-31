# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Common Custom Membership',
    'version': '11.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Membership',
    "sequence": 3,
    'summary': 'Manage members',
    'complexity': "easy",
    'author': 'By Innovik',
    'website': 'http://www.openeducat.org',
    'depends': ['base','contacts', 'document', 'website'],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'security/res.lang.csv',
        'views/district_view.xml',
        'views/union_view.xml',
        'views/panchayat_view.xml',
        'views/members_view.xml',
        'views/admission_register_view.xml',
        'views/admission_view.xml',
        'views/admission_member_sequence.xml',
        'views/group_sms_view.xml',
        'views/res_partner_view.xml',
        'views/hide_apps.xml',
        'views/multimedia_view.xml',
        'wizard/language_view.xml',
        'wizard/whatsapp_message_view.xml',
        'wizard/member_create_user_wizard_view.xml',
	
        'views/data.xml',
        'views/template.xml',


    ],
    'images': [
    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

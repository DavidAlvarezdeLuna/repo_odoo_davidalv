# -*- coding: utf-8 -*-
{
    'name': "devmeet",

    'summary': """
        Mi modulo de DevMeet""",

    'description': """
        Es la practica entregable de DevMeet
    """,

    'author': "David Alvarez",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Practica',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'demo/developers.xml',
    ],
}

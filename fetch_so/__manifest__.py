# -*- coding: utf-8 -*-

{
    'name': "Fetch sale orders",
    'version': '18.0.1.0',
    'depends': ['base', 'sale','contacts','product'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
           This module helps to migrate odoo 17 sale orders into odoo 18
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/fetch_sale_order_views.xml',
    ],

    'application': True,
    'license': 'LGPL-3',
}

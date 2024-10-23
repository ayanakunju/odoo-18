# -*- coding: utf-8 -*-

{
    'name': "Account Recurring Payments",
    'version': '18.0.1.0',
    'depends': ['base', 'account'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
           This module create the account recurring payments
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/recurring_payment_views.xml',
        'views/journal_entry_wizard.xml',
    ],

    'application': True,
    'license': 'LGPL-3',
}

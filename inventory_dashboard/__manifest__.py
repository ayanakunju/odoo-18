# -*- coding: utf-8 -*-

{
    'name': "Inventory Dashboard",
    'version': '18.0.1.0',
    'depends': ['base', 'stock','stock_account'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
           This module creates an inventory dashboard 
    """,

    'data': [
        'views/inventory_dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_dashboard/static/src/js/inventory_dashboard.js',
            'inventory_dashboard/static/src/xml/inventory_dashboard.xml',
            'https://cdn.jsdelivr.net/npm/chart.js',
        ],
    },

    'application': True,
    'license': 'LGPL-3',
}

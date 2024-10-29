# -*- coding: utf-8 -*-

{
    'name': "Pos Remove Order Line",
    'version': '18.0.3.0.0',
    'depends': ['base', 'point_of_sale'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    This module removes the order line in the pos.
    """,

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_remove_order_line/static/src/js/remove_button.js',
            'pos_remove_order_line/static/src/js/remove_order_line.js',
            'pos_remove_order_line/static/src/xml/remove_button.xml',
            'pos_remove_order_line/static/src/xml/remove_order_line.xml',
        ]
    },
    'application': True,

}

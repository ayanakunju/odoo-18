# -*- coding: utf-8 -*-
{
    'name': "Slider Widget",
    'version': '18.0.1.0',
    'depends': ['base', 'product'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
            This module creates a field widget that helps the user to pick an 
            integer value using the slider inside the ptoduct
    """,

    'data': [
        'views/range_field_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'slider_widget/static/src/xml/range_slider.xml',
            'slider_widget/static/src/js/range_slider.js',
        ],
    },

    'application': True,
    'license': 'LGPL-3',
}


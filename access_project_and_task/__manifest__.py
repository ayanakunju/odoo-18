# -*- coding: utf-8 -*-
{
    'name': "Restrict Project And Task",
    'version': '18.0.1.0',
    'depends': ['base', 'project'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
           This module restrict project and task on specific groups
    """,

    'data': [
        'security/project_task_security.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
    ],

    'application': True,
    'license': 'LGPL-3',
}


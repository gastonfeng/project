# -*- coding: utf-8 -*-

{
    'name': "Odoo Service desk",
    'version': '9.0.1.0.0',
    'depends': [
        'project'
    ],
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Project',
    'description': """
This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [
        'views/service_view.xml',
        'views/service_project_issue_view.xml',
        'views/service_project_task_view.xml',
        'views/service_project_timesheet_view.xml',
        'views/service_project_project_view.xml',
    ],
}
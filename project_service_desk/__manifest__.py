# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
{
    'name': "Odoo Service desk",
    'version': '10.0.1.0.0',
    'author': 'AbAKUS it-solutions SARL',
    'license': 'AGPL-3',
    'depends': [
        'project',
        'project_issue_improvements',
        'project_generic_close_stage',
        'hr_analytic_timesheet_improvements'
    ],
    'website': 'http://www.abakusitsolutions.eu',
    'category': 'Project',
    'data': [
        'views/service_view.xml',
        'views/service_project_issue_view.xml',
        'views/service_project_task_view.xml',
        'views/service_project_timesheet_view.xml',
        'views/service_project_project_view.xml',
    ],
}

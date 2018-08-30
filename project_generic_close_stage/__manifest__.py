# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
{
    'name': "Project Generic Close Stage",
    'summary': 'Project Generic Close Stage',
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Project',
    'license': 'AGPL-3',
    'version': '10.0.1.0.0',
    'depends': [
        'base',
        'project',
        'project_issue'
    ],
    'data': [
        'views/project_task_type.xml',
        'views/project_task.xml',
        'views/project_issue.xml',
    ],
    'application': False,
    'installable': True,
}

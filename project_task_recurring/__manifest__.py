# (c) AbAKUS IT Solutions
{
    'name': "Project Task Recurring",
    'version': '11.0.1.0.0',
    'author': "AbAKUS it-solutions SARL",
    'license': 'AGPL-3',
    'summary': "Create recurring tasks",
    'website': "http://www.abakusitsolutions.eu",
    'depends': [
        'project'
    ],
    'category': 'Project',
    'data': [
        'views/project_task_model_view.xml',
        'views/project_task_view.xml',

        'data/ir_cron.xml',

        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}

{
    'name': "New Fields on Project Tasks",
    'version': '9.0.1.0',
    'depends': [
        'project'
    ],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Project',
    'data': [
        'view/project_task_view.xml',
    ],
    'depends': [
        'base',
        'project',
        'sale_service',
        'project_issue',
        'project_generic_close_stage'
    ],
}

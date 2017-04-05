from openerp import models, fields, api, _

class project_service_desk(models.Model):
    _inherit = ['project.project']

    project_type = fields.Selection([('support', 'Support'), ('installation', 'Installation'), ('internal', 'Internal'), ('development', 'Development'), ('other', 'Other')], 'Type of Project')

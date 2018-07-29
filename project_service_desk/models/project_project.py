# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
from odoo import models, fields, api, _


class ProjectServiceDesk(models.Model):
    _inherit = ['project.project']

    project_type = fields.Selection([
        ('support', 'Support'),
        ('installation', 'Installation'),
        ('internal', 'Internal'),
        ('development', 'Development'),
        ('other', 'Other')], 'Type of Project')

    defaults = {
        'project_type ': lambda self: self._get_default_project_type()
    }

    def _get_default_project_type(self):
        context = dict(self.env.context)
        if 'default_project_type' in context:
            if context['default_project_type']:
                return context['default_project_type']
        return False

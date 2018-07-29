# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProjectTaskServiceDesk(models.Model):
    _inherit = ['project.task']

    project_type = fields.Selection(related='project_id.project_type', store=True)
    project_id = fields.Many2one(default=lambda s: s._get_default_project_id())
    stage_id = fields.Many2one(default=lambda s: s._get_default_stage_id())
    partner_id = fields.Many2one(default=lambda s: s._get_default_partner())

    def _get_default_project_id(self):
        context = dict(self.env.context)
        if 'default_analytic_account_id' in context:
            analytic_account = self.pool.get('account.analytic.account').browse(context['default_analytic_account_id'])
            if analytic_account and len(analytic_account.project_ids) > 0:
                project_id = analytic_account.project_ids[0]
            if analytic_account and len(analytic_account.subscription_ids) > 0:
                if analytic_account.subscription_ids[0].project_id:
                    project_id = analytic_account.subscription_ids[0].project_id
        if project_id:
            return project_id.id
        return False

    def _get_default_stage_id(self):
        context = dict(self.env.context)
        default_project_id = context.get('default_project_id')
        if default_project_id:
            return self.stage_find([], default_project_id, [('fold', '=', False)])
        if 'default_analytic_account_id' in context:
            analytic_account = self.pool.get('account.analytic.account').browse(context['default_analytic_account_id'])
            if analytic_account and len(analytic_account.project_ids) > 0:
                project_id = analytic_account.project_ids[0]
            if analytic_account and len(analytic_account.subscription_ids) > 0:
                if analytic_account.subscription_ids[0].project_id:
                    project_id = analytic_account.subscription_ids[0].project_id
        if project_id:
            return self.stage_find([], default_project_id, [('fold', '=', False)])
        return False

    def _get_default_partner(self):
        context = dict(self.env.context)
        if 'default_project_id' in context:
            project = self.pool.get('project.project').browse(context['default_project_id'])
            if project and project.partner_id:
                return project.partner_id.id
        if 'default_analytic_account_id' in context:
            analytic_account = self.env['account.analytic.account'].browse(context['default_analytic_account_id'])
            if analytic_account and len(analytic_account.project_ids) > 0:
                project_id = analytic_account.project_ids[0]
            if analytic_account and len(analytic_account.subscription_ids) > 0:
                if analytic_account.subscription_ids[0].project_id:
                    project_id = analytic_account.subscription_ids[0].project_id
        if project_id:
            return project_id.partner_id.id
        return False

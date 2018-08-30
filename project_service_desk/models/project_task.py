# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from pprint import pformat
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
        project_id = None
        context = dict(self.env.context)
        if 'default_analytic_account_id' in context:
            analytic_account = self.pool.get('account.analytic.account').browse(context['default_analytic_account_id'])
            if analytic_account and len(analytic_account.project_ids) > 0:
                project_id = analytic_account.project_ids[0]
            if analytic_account and len(analytic_account.subscription_ids) > 0:
                if analytic_account.subscription_ids[0].project_id:
                    project_id = analytic_account.subscription_ids[0].project_id
        if project_id is not None:
            return project_id.id
        return False

    def _get_default_stage_id(self):
        project_id = None
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
        if project_id is not None:
            return self.stage_find([], default_project_id, [('fold', '=', False)])
        return False

    def _get_default_partner(self):
        project_id = None
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

        if project_id is not None:
            return project_id.partner_id.id
        return False


class ProjectTaskStageMrp(models.Model):
    """ Override project.task.type model to add a 'closed' boolean field allowing
        to know that tasks in this stage are considered as closed. Indeed since
        OpenERP 8.0 status is not present on tasks anymore, only stage_id.

        Odoo 10.0 has completely remove this flag and not brought back status on a task.
        This is code previously (9.0) appearing in sale_service/models/sale_service.py
        """
    _inherit = 'project.task.type'

    closed = fields.Boolean('Is a close stage', help="Tasks in this stage are considered as closed.", default=False)

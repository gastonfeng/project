# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountAnalyticLineServiceDesk(models.Model):
    _inherit = ['account.analytic.line']

    issue_state = fields.Many2one(related='issue_id.stage_id')
    task_state = fields.Many2one(related='task_id.stage_id')

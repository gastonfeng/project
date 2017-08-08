from openerp import models, fields, api, _
from openerp.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)

class account_analytic_line_service_desk(models.Model):
    _inherit = ['account.analytic.line']

    issue_state = fields.Selection(related='issue_id.state', string="Issue State")
    task_state = fields.Selection(related='task_id.state', string="Task State")
from openerp import models, fields, api, _
from openerp.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)

class account_analytic_line_service_desk(models.Model):
    _inherit = ['account.analytic.line']

    issue_state = fields.Many2one(related='issue_id.stage_id', string="Issue State")
    task_state = fields.Many2one(related='task_id.stage_id', string="Task State")

    @api.multi
    def close_task_issue(self):
        self.ensure_one()
        if self.issue_id:
            self.issue_id.action_close()
        elif self.task_id:
            self.task_id.action_close()

    @api.multi
    def delete_worklog(self):
        self.unlink()
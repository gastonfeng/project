from openerp import models, fields, api, _
from openerp.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)

class account_analytic_line_service_desk(models.Model):
    _inherit = ['account.analytic.line']

    def _get_default_project(self):
        if self.account_id:
            if len(self.account_id.project_ids) > 0:
                return self.account_id.project_ids[0].id
        return False

    project_id = fields.Many2one('project.project', string="Project", default=lambda self: self._get_default_project()) # Only used to search on the form and directlty set the correct Analytic Account
    issue_state = fields.Many2one(related='issue_id.stage_id', string="Issue State")
    task_state = fields.Many2one(related='task_id.stage_id', string="Task State")

    @api.multi
    @api.onchange('project_id')
    def set_correct_analytic_account(self):
        for line in self:
            if line.project_id:
                line.account_id = line.project_id.analytic_account_id

    @api.model
    def write(self, vals):
        if 'project_id' not in vals:
            _logger.debug("TEST\n\n NO PROJECT GIVEN")
            project_id = self.env['project.project'].search([('analytic_account_id', '=', vals['account_id'])])
            _logger.debug("TEST\n\n PROJECT %s", project_id)
            vals.update({'project_id': project_id.id})
        rec = super(account_analytic_line_service_desk, self).write(vals)
        return rec

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
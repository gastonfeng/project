# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'project.project'

    display_name = fields.Char(string='Name', compute='_compute_display_name')

    task_planned_hours_sum = fields.Float(string="Planned Hours Sum for Tasks",
                                          compute='_compute_task_planned_hours_sum')
    task_effective_hours_sum = fields.Float(string="Effective Hours Sum for Tasks",
                                            compute='_compute_task_effective_hours_sum')
    issue_effective_hours_sum = fields.Float(string="Effective Hours Sum for Issues",
                                             compute='_compute_issues_effective_hours_sum')
    total_effective_hours_sum = fields.Float(compute='_compute_total_effective_hours_sum')
    total_timesheets_hours_sum = fields.Float(compute='_compute_total_timesheets_hours_sum')
    total_difference_estimation_effective_sum = fields.Float(
        string="Total difference between estimation and effective",
        compute='_compute_total_difference_estimation_effective_sum')
    total_timesheets_not_linked_sum = fields.Float(string="Total timesheets not linked to task or issue",
                                                   compute='_compute_total_timesheets_not_linked_sum')

    @api.multi
    @api.depends('name')
    def _compute_display_name(self):
        for proj in self:
            #  add completion percentage in percent
            completion_percent = 0.0
            if proj.task_planned_hours_sum > 0:
                completion_percent = (proj.total_timesheets_hours_sum * 100) / proj.task_planned_hours_sum
            proj.display_name = proj.name + " - [{:.1f}% - {:.1f}h / {:.1f}h]".format(
                completion_percent,
                proj.total_timesheets_hours_sum,
                proj.task_planned_hours_sum
            )

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            completion_percent = 0.0
            if record.task_planned_hours_sum > 0:
                completion_percent = (record.total_timesheets_hours_sum * 100) / record.task_planned_hours_sum
            name = record.name + " - [{:.1f}% - {:.1f}h / {:.1f}h]".format(
                completion_percent,
                record.total_timesheets_hours_sum,
                record.task_planned_hours_sum
            )
            result.append((record.id, name))
        return result

    @api.multi
    def _compute_task_planned_hours_sum(self):
        for proj in self:
            proj.task_planned_hours_sum = sum([task.planned_hours for task in proj.task_ids])

    @api.multi
    def _compute_task_effective_hours_sum(self):
        for proj in self:
            proj.task_effective_hours_sum = sum([task.effective_hours for task in proj.task_ids])

    @api.multi
    def _compute_issues_effective_hours_sum(self):
        for proj in self:
            issues_sum = 0
            for issue in proj.issues:
                issues_sum = issues_sum + sum([timesheet.unit_amount for timesheet in issue.timesheet_ids])
            proj.issue_effective_hours_sum = issues_sum

    @api.multi
    def _compute_total_effective_hours_sum(self):
        for proj in self:
            proj.total_effective_hours_sum = proj.task_effective_hours_sum + proj.issue_effective_hours_sum

    @api.multi
    def _compute_total_timesheets_hours_sum(self):
        for proj in self:
            timesheet_ids = proj.env['account.analytic.line'].search([
                ('account_id', '=', proj.analytic_account_id.id),
                ('is_timesheet', '=', True)])
            proj.total_timesheets_hours_sum = sum([timesheet.unit_amount for timesheet in timesheet_ids])

    @api.multi
    def _compute_total_difference_estimation_effective_sum(self):
        for proj in self:
            proj.total_difference_estimation_effective_sum = \
                abs(proj.task_effective_hours_sum - proj.task_planned_hours_sum)

    @api.multi
    def _compute_total_timesheets_not_linked_sum(self):
        for proj in self:
            proj.total_timesheets_not_linked_sum = \
                abs(proj.total_timesheets_hours_sum - proj.total_effective_hours_sum)

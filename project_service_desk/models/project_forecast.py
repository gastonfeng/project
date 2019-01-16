# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions

from openerp import models, fields, api, exceptions, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)


class ProjectForecast(models.Model):
    _inherit = ['project.forecast']

    planned_time = fields.Selection([('am', 'AM'), ('pm', 'PM'), ('am_pm', 'AM+PM'), ('specific', 'Specific time')], string='Planned on')
    issue_ids = fields.Many2many('project.issue', string="Issues", domain="[('project_id', '=', project_id)]")
    task_ids = fields.Many2many('project.task', string="Tasks", domain="[('project_id', '=', project_id)]")
    leave_id = fields.Many2one('hr.holidays', string="Leave", domain="[('type', '=', 'remove'), ('user_id', '=', user_id)]")
    project_id = fields.Many2one('project.project', string="Project")
    comment = fields.Text(string="Comment")

    tasks_planned_hours = fields.Float(string="Planned time on tasks", compute='_compute_total_planned_hours')

    @api.multi
    @api.onchange('task_ids')
    def _compute_total_planned_hours(self):
        for forecast in self:
            forecast.tasks_planned_hours = 0
            for task in forecast.task_ids:
                forecast.tasks_planned_hours += task.planned_hours

    @api.one
    @api.onchange('planned_time')
    def planned_time_changed(self):
        calendar_ids = self.env['resource.calendar'].search([('company_id', '=', self.user_id.company_id.id)])

        worktime = {
            'morning': 8.5,
            'midday': 13.5,
            'evening': 17.5
        }

        start_date = datetime.strptime(self.start_date, DEFAULT_SERVER_DATETIME_FORMAT)
        end_date = datetime.strptime(self.end_date, DEFAULT_SERVER_DATETIME_FORMAT)

        if len(calendar_ids) > 0:
            for attendance in calendar_ids.attendance_ids:
                if int(attendance.dayofweek) == start_date.weekday():
                    worktime['morning'] = attendance.hour_from
                    worktime['midday'] = (attendance.hour_to + attendance.hour_from) / 2
                    worktime['evening'] = attendance.hour_to
                    break
    
        if self.planned_time == 'am':
            self.start_date = start_date.replace(hour=int(worktime['morning'] - 1))
            self.end_date = end_date.replace(hour=int(worktime['midday'] - 1))
        elif self.planned_time == 'pm':
            self.start_date = start_date.replace(hour=int(worktime['midday'] - 1))
            self.end_date = end_date.replace(hour=int(worktime['evening'] - 1))
        elif self.planned_time == 'am_pm':
            self.start_date = start_date.replace(hour=int(worktime['morning'] - 1))
            self.end_date = start_date.replace(hour=int(worktime['evening'] - 1))

    @api.one
    @api.onchange('leave_id')
    def leave_changed(self):
        if self.leave_id:
            self.start_date = self.leave_id.date_from
            self.end_date = self.leave_id.date_to          
            

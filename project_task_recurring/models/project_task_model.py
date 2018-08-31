# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, _
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class ProjectTaskModel(models.Model):
    _name = 'project.task.model'
    _description = "Task model"
    _inherit = ['mail.thread']

    name = fields.Char(string="Name", required=True)
    recurring_rule_type = fields.Selection([('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('year', 'Year')], string='Recurrency', required=True)
    recurring_interval = fields.Integer(string="Repeat every", required=True, default=1)
    start_date = fields.Date(string="Start at", required=True, default=date.today())
    last_created_date = fields.Date(string="Last task created on")
    project_id = fields.Many2one('project.project')
    description = fields.Html(string="Description")
    user_id = fields.Many2one('res.users', string="Assigned to")
    active = fields.Boolean(string="Active", default=True)
    task_ids = fields.One2many('project.task', 'task_model_id', string="Tasks")
    task_count = fields.Integer(compute='_compute_task_count', string='Tasks')

    def _compute_task_count(self):
        for model in self:
            model.task_count = len(model.task_ids)

    @api.multi
    def action_create_task(self):
        for model in self:
            if model.active:
                self.env['project.task'].create({
                    'name': model.name,
                    'project_id': model.project_id.id,
                    'description': model.description,
                    'user_id': model.user_id.id,
                    'task_model_id': model.id,
                })
                model.last_created_date = date.today()

    @api.model
    def cron_create_tasks(self):
        model_ids = self.env['project.task.model'].search([])
        for model in model_ids:
            # No task created yeat
            if model.task_count == 0 or not model.last_created_date:
                if model.start_date <= datetime.now().date().strftime('%Y-%m-%d'):
                    _logger.debug("\n First date, create task !")
                    model.action_create_task()
                    continue
                continue
            # Already created
            last_date = datetime.strptime(model.last_created_date, "%Y-%m-%d")
            if model.recurring_rule_type == 'day':
                new_date = last_date + relativedelta(days=+model.recurring_interval)
            elif model.recurring_rule_type == 'week':
                new_date = last_date + relativedelta(weeks=+model.recurring_interval)
            elif model.recurring_rule_type == 'month':
                new_date = last_date + relativedelta(months=+model.recurring_interval)
            elif model.recurring_rule_type == 'year':
                new_date = last_date + relativedelta(years=+model.recurring_interval)

            if new_date.strftime('%Y-%m-%d') < datetime.now().date().strftime('%Y-%m-%d'):
                model.action_create_task()
                continue

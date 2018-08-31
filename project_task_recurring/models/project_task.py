# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, _
from datetime import date
from datetime import timedelta

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_model_id = fields.Many2one('project.task.model', string="Model")
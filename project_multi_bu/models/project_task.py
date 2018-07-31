# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)


class ProjectTaskBU(models.Model):

    _inherit = 'project.task'

    def compute_default_business_unit_id(self):
        """ alternatively use self.env.user.business_unit_id in a lambda function """
        return self.env['res.users'].browse(self.env.uid).business_unit_id.id

    business_unit_id = fields.Many2one('business.unit',
                                       string='Business Unit',
                                       default=compute_default_business_unit_id)

# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ProjectIssueAssignItself(models.Model):
    _inherit = ['project.issue']

    @api.multi
    def assign_to_me(self):
        for issue in self:
            issue.user_id = self.env.user.id

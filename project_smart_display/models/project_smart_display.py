# -*- coding: utf-8 -*-
# This code has been written
# by AbAKUS it-solutions SARL
# in Luxembourg 2018

from openerp import models, fields, api, _
from openerp.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)

class ProjectSmartDisplay(models.Model):
    _name = 'project.smart.display'

    name = fields.Char(required=True, string="Name")
    ip_address = fields.Char(string="IP address")
    user_ids = fields.Many2many('res.users', string="Users")
    active = fields.Boolean(string="Active", default=True)
    page_ids = fields.Many2many('project.smart.display.page', string="Pages")

class ProjectSmartDisplayPage(models.Model):
    _name = 'project.smart.display.page'

    name = fields.Char(required=True, string="Name")
    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying pages')
    mode = fields.Selection([('iframe', 'Iframe'), ('smart_dashboard', 'Smart Dashboard')], string="Mode", required=True)
    iframe_url = fields.Char(string="Iframe URL")
    widget_ids = fields.One2many('project.smart.display.widget', 'page_id', string="Widgets")

class ProjectSmartDisplayWidget(models.Model):
    _name = 'project.smart.display.widget'

    name = fields.Char(required=True, string="Name")
    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying widgets')
    page_id = fields.Many2one('project.smart.display.page', required=True)

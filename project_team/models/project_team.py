# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class ProjectTeam(models.Model):
    _name = 'project.team'
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    team_member_ids = fields.Many2many('res.users', 'project_team_user_rel', 'team_id', 'uid', 'Project Members')
    team_leader_id = fields.Many2one('res.users', string="Team Leader")#, domain="[('id', 'in', team_member_ids)]")
    company_id = fields.Many2one('res.company', string="Company")
    active = fields.Boolean(string="Active")

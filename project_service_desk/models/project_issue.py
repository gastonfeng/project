from openerp import models, fields, api, _
from openerp.exceptions import UserError


import logging
_logger = logging.getLogger(__name__)

class project_issue_service_desk(models.Model):
    _inherit = ['project.issue']

    def _get_default_project_id(self, cr, uid, context=None):
        project_id = False
        if context is None:
            context = {}
        if 'default_analytic_account_id' in context:
            analytic_account = self.pool.get('account.analytic.account').browse(cr, uid, context['default_analytic_account_id'], context=context)
            if analytic_account and len(analytic_account.project_ids) > 0:
                project_id = analytic_account.project_ids[0]
            if analytic_account and len(analytic_account.subscription_ids) > 0:
                if analytic_account.subscription_ids[0].project_id:
                    project_id = analytic_account.subscription_ids[0].project_id
        if project_id != False:
            return project_id.id
        raise UserError(_('You have not selected a Project (or the selected project is not valid). This way, the newly created Issue (%s) is not linked to the correct Project. Please, correct this.') % self.name)
        return False

    def _get_default_stage_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        default_project_id = context.get('default_project_id')
        if default_project_id:
            return self.stage_find(cr, uid, [], default_project_id, [('fold', '=', False)], context=context)
        if 'default_analytic_account_id' in context:
            analytic_account = self.pool.get('account.analytic.account').browse(cr, uid, context['default_analytic_account_id'], context=context)
            if analytic_account and len(analytic_account.project_ids) > 0:
                project_id = analytic_account.project_ids[0]
                return self.stage_find(cr, uid, [], project_id.id, [('fold', '=', False)], context=context)
            if analytic_account and len(analytic_account.subscription_ids) > 0:
                if analytic_account.subscription_ids[0].project_id:
                    project_id = analytic_account.subscription_ids[0].project_id
                    return self.stage_find(cr, uid, [], project_id.id, [('fold', '=', False)], context=context)
        return False

    _defaults = {
        'project_id': lambda s, cr, uid, c: s._get_default_project_id(cr, uid, context=c),
        'stage_id': lambda s, cr, uid, c: s._get_default_stage_id(cr, uid, c),
    }

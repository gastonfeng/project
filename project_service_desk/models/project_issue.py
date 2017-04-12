from openerp import models, fields, api, _
from openerp.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class project_issue_service_desk(models.Model):
    _inherit = ['project.issue']

    def _get_default_project_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        
        if 'default_analytic_account_id' in context:
            analytic_account = self.pool.get('account.analytic.account').browse(cr, uid, context['default_analytic_account_id'], context=context)
            if analytic_account and analytic_account.first_subscription_id.project_id:
                return analytic_account.first_subscription_id.project_id.id
            raise UserError(_('The selected Project (%s) is not linked to a specific Project in Odoo. This way, the newly created Issue is not linked to the correct Project. Please, correct this.') % analytic_account.name)
        return False

    _defaults = {
        'project_id': lambda s, cr, uid, c: s._get_default_project_id(cr, uid, context=c),
    }

    
from openerp import models, fields, api
from openerp import _
import logging
_logger = logging.getLogger(__name__)

class project_issue_improvements(models.Model):
    _inherit = ['project.issue']

    

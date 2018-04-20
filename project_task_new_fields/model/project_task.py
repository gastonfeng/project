
from openerp import models, fields


class AnalyticAccount(models.Model):
    _inherit = 'project.task'

    customer_feedback = fields.Text(string="Customer Feedback")
    sale_order_id = fields.Many2one(related='sale_line_id.order_id', string="Origin Sale order", readonly=True)

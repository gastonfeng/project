# -*- coding: utf-8 -*-
# This code has been written
# by AbAKUS it-solutions SARL
# in Luxembourg 2018

import logging
from openerp import http, _
from openerp.exceptions import AccessError
from openerp.http import request

_logger = logging.getLogger(__name__)

class SmartDisplayPage(http.Controller):

    @http.route([
        '/smartdisplay/display/<model("project.smart.display"):display_id>',
    ], type='http', auth="user", website=True)
    def smart_display_web_page(self, page=0, display_id=None, search='', ppg=False, **post):
        display_ids = http.request.env['project.smart.display'].sudo().search([('id', '=', display_id.id)])
        return http.request.render('project_smart_display.smart_display_web_page', {'display': display_ids})
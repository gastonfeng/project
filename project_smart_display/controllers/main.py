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
    ], type='http', auth="public", website=True)
    def smart_display_web_page(self, page=0, display_id=None, search='', ppg=False, **post):
        display_ids = http.request.env['project.smart.display'].sudo().search([('id', '=', display_id.id)])
        return http.request.render('project_smart_display.smart_display_web', {'display': display_ids})

    @http.route([
        '/smartdisplay/getdisplay/'],
                type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def get_display(self, display_id, *kw):
        """ Ajax call to get page from id """
        if display_id:
            display = request.env['project.smart.display'].sudo().search([('id', '=', display_id)])
            
            if not display or len(display) != 1:
                return {'display_id': -1}
            else:
                return {
                    'display_id': display.id,
                    'name': display.name,
                    'page_count': len(display.page_ids),
                    'delay': display.delay,
                }

    @http.route([
        '/smartdisplay/getnextpage/'],
                type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def get_next_page(self, display_id, index, *kw):
        """ Ajax call to get page for display """
        if display_id:
            display = request.env['project.smart.display'].sudo().search([('id', '=', display_id)])
            if not display or len(display) != 1 or len(display.page_ids) == 0:
                return {'page_id': -1}
            if index < 0:
                index = 0
            if index >= len(display.page_ids):
                index = 0
            next_page = display.page_ids[index]
            return {
                'page_id': next_page.id,
                'name': next_page.name,
                'sequence': next_page.sequence,
                'mode': next_page.mode,
                'iframe_url': next_page.iframe_url,
                'diaplay_page_count': len(display.page_ids),
                'display_delay': display.delay,
            }
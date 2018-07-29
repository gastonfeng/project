# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import HTMLParser
from odoo import models


class MailMailUtilities(models.Model):
    _inherit = ['mail.mail']

    @staticmethod
    def unescapeHTML(text):
        return HTMLParser.HTMLParser().unescape(text)

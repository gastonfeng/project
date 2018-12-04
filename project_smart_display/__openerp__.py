# -*- coding: utf-8 -*-
# This code has been written
# by AbAKUS it-solutions SARL
# in Luxembourg 2018

{
    'name': "Smart Displays Management at AbAKUS it-solutions",
    'version': '9.0.1.0.0',
    'depends': [
        'project_service_desk',
    ],
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Project',
    'description': """
Smart Displays Management at AbAKUS it-solutions

This modules creates web pages that dynamically changes to present web pages or statistic dashboards for the Team @ AbAKUS it-solutions Eupen

This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [
        'views/project_smart_display.xml',

        'security/ir.model.access.csv',
    ],
}
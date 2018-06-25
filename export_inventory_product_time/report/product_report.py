# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo import fields, api, tools, models, _
from odoo.exceptions import UserError, Warning, RedirectWarning, ValidationError

from openerp.tools.sql import drop_view_if_exists
from datetime import date, timedelta

class ProductReport(models.AbstractModel):
    _name = 'report.export_inventory_product_time.report_product'
    #  nombre del report.xml . nombre de la carpeta del modulo . nombre del template
    #def render_html(self, ids, data=None, context=None):
    @api.model
    def render_html(self, docids, data=None): # data es eldata que recibo del metodo "print_report" de summary_report(models.Model)

        report_obj = self.env['report']
        export_inventory_obj = self.env['wizard.export.inventory.product.time']
        report = report_obj._get_report_from_name('export_inventory_product_time.report_product')
        docs = export_inventory_obj.browse(data['context']['active_id'])
        docargs = {
            'doc_ids': data['active_ids'],# Lista de id o ids del modelo del reporte
            'doc_model': report.model, #modelo del reporte
            'docs': docs, #objeto del modelo del reporte
            'data': data,
        }
        return report_obj.render('export_inventory_product_time.report_product', docargs)




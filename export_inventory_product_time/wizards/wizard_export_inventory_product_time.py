# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError,UserError
import tempfile
import shutil
import base64
import os
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import dicttoxml
import  sys
import xmltodict
from lxml import etree
import locale
import time
from odoo import osv
from datetime import datetime, date, time, timedelta
from odoo import api, fields, models
import csv
import StringIO
from odoo import http
import unicodedata
try:
    import xlwt
except ImportError:
    xlwt = None
import re
from cStringIO import StringIO


class WizardExportInventoryProductTime(models.TransientModel):
    _name = "wizard.export.inventory.product.time"
    _description = "wizard.export.inventory.product.time"
               
    
    date_init = fields.Date('Fecha Inicio')
    date_end = fields.Date( 'Fecha Fin', required=True,  default=lambda self: datetime.today())
    company_id = fields.Many2one('res.company', 'Company',  default=lambda self: self.env.user.company_id)
    
    @api.multi
    def get_origin(self,data):
        
        context = dict(self._context or {})
        active_ids = data.get('active_ids', False)
        product_template_ids = self.env['product.template'].browse(active_ids)
        move_obj = self.env['account.move.line']
        
        lines_total = []
        #  Recorro los productos seleccionados
        for product_t in product_template_ids:
            lines = []
            # toma todos los movimientos del productos menores a la fecha final
            move_lines_ids = move_obj.search([('product_id','=', product_t.product_variant_id.id), ('date','<=', self.date_end)],order='date')
            if move_lines_ids:
                total_debit = 0.0
                total_credit = 0.0
                total_inventory = 0.0
                last_date = move_lines_ids[0].date
                q_move_lines = len(move_lines_ids)
                
                count_move_lines = 0
                
                while count_move_lines <= q_move_lines:
                    count=0
                    if count_move_lines == 0:
                        move_lines_date_ids = move_obj.search([('product_id','=', product_t.product_variant_id.id),('date','=',last_date)],order='date')
                        count_move_lines +=1
                    else:
                        c=0
                        for line in move_lines_ids:
                            c+=1
                            if c==count_move_lines:
                                last_date = line.date
                        move_lines_date_ids = move_obj.search([('product_id','=', product_t.product_variant_id.id),('date','=',last_date)],order='date')
                        
                    q_lines_date = len(move_lines_date_ids)
                    # valido todas las lineas que tienen la misma fecha
                    for line in move_lines_date_ids:
                        count+=1
                        if (line.invoice_id.type == 'in_invoice') or (line.invoice_id.type == 'out_refund'):
                            total_debit += line.quantity
                            total_inventory += line.quantity
                        else:
                            total_credit += line.quantity
                            total_inventory -= line.quantity
                        if count == q_lines_date:
                            vals = {'product_id': str(product_t.product_variant_id.default_code),
                                    'product_name': product_t.product_variant_id.name,
                                    'date': line.date,
                                    'quantity_purchase': total_debit,
                                    'quantity_sale': total_credit,
                                    'quantity_inv': total_inventory}
                            lines.append(vals)
                            total_debit = 0.0
                            total_credit = 0.0
                    if count>0:
                        count_move_lines+=count
                    else:
                        count_move_line+=1
            
            if lines:
                qty_lines = len(lines)
                cnt = 0
                for l in lines[:]:
                    cnt += 1
                    if cnt != qty_lines:
                        lines.remove(l)
                        
            lines_total = lines_total + lines
        
                
        data.update({'lines':lines_total})
        #data.update(self.read(['date_from', 'date_to'])[0])
        return self.env['report'].get_action(self, 'export_inventory_product_time.report_product', data=data)
        return True


    def generate_file(self,data):
            
        context = dict(self._context or {})
        active_ids = data.get('active_ids', False)
        product_template_ids = self.env['product.template'].browse(active_ids)
        move_obj = self.env['account.move.line']
        lines_total = []
        #  Recorro los productos seleccionados
        for product_t in product_template_ids:
            lines = []
            # toma todos los movimientos del productos menores a la fecha final
            move_lines_ids = move_obj.search([('product_id','=', product_t.product_variant_id.id), ('date','<=', self.date_end)],order='date')
            if move_lines_ids:
                total_debit = 0.0
                total_credit = 0.0
                total_inventory = 0.0
                last_date = move_lines_ids[0].date
                q_move_lines = len(move_lines_ids)
                
                count_move_lines = 0
                
                while count_move_lines <= q_move_lines:
                    count=0
                    if count_move_lines == 0:
                        move_lines_date_ids = move_obj.search([('product_id','=', product_t.product_variant_id.id),('date','=',last_date)],order='date')
                        count_move_lines +=1
                    else:
                        c=0
                        for line in move_lines_ids:
                            c+=1
                            if c==count_move_lines:
                                last_date = line.date
                        move_lines_date_ids = move_obj.search([('product_id','=', product_t.product_variant_id.id),('date','=',last_date)],order='date')
                        
                    q_lines_date = len(move_lines_date_ids)
                    # valido todas las lineas que tienen la misma fecha
                    for line in move_lines_date_ids:
                        count+=1
                        if (line.invoice_id.type == 'in_invoice') or (line.invoice_id.type == 'out_refund'):
                            total_debit += line.quantity
                            total_inventory += line.quantity
                        else:
                            total_credit += line.quantity
                            total_inventory -= line.quantity
                        if count == q_lines_date:
                            vals = {'product_id': str(product_t.product_variant_id.default_code),
                                    'product_name': product_t.product_variant_id.name,
                                    'date': line.date,
                                    'quantity_purchase': total_debit,
                                    'quantity_sale': total_credit,
                                    'quantity_inv': total_inventory}
                            lines.append(vals)
                            total_debit = 0.0
                            total_credit = 0.0
                    if count>0:
                        count_move_lines+=count
                    else:
                        count_move_line+=1
        
            if lines:
                qty_lines = len(lines)
                cnt = 0
                for l in lines[:]:
                    cnt += 1
                    if cnt != qty_lines:
                        lines.remove(l)
                        
            lines_total = lines_total + lines
            
        path = '/tmp/file_%s.csv'% (datetime.today())
        fp = StringIO()
        with open(path, 'w') as csvfile:
            csvfile.write("Reporte de; Inventario ;de Productos;\n")
            csvfile.write("Fecha:;{1} \n".format("",self.date_end ))
            #csvfile.write("Codigo;Producto;Fecha;Cantidad Comprada;Cantidad Vendida;Cantidad en Inventario \n")
            csvfile.write("Codigo;Producto;Cantidad en Inventario \n")
            
            for lin in lines_total:
                #csvfile.write("{0};{1};{2};{3};{4};{5} \n".format(lin['product_id'], lin['product_name'], lin['date'], lin['quantity_purchase'], lin['quantity_sale'], lin['quantity_inv']))
                csvfile.write("{0};{1};{2} \n".format(lin['product_id'], lin['product_name'], lin['quantity_inv']))

        fp.close()
        csvfile.close()
        arch = open(path, 'r').read()
        data = base64.encodestring(arch)
        attach_vals = {
                        'name':'Reporte de Inventario Productos %s.csv' % (datetime.today().strftime("%d-%m-%Y")),
                        'datas':data,
                        'datas_fname':'File#_%s.csv' % (datetime.today().strftime("%d-%m-%Y")),
        }
        doc_id = self.env['ir.attachment'].create(attach_vals)
        return {
                'type' : "ir.actions.act_url",
                'url': "web/content/?model=ir.attachment&id="+str(doc_id.id)+"&filename_field=datas_fname&field=datas&download=true&filename="+str(doc_id.name),
                'target': "self",
        }
        
        

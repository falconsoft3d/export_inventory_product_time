# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2016 Steigend IT Solutions
#    For more details, check COPYRIGHT and LICENSE files
#
##############################################################################
{
    'name': "Reporte Inventario Producto por Fecha",
    'summary': """
        Crea un reporte pdf o xml del inventario de un producto en determinada fecha.""",
    'description': """
    Este módulo crear un reporte pdf o xml del inventario de un producto en determinada fecha.
    """,
    'author': 'Falcón Solutions',
    'website': 'http://www.falconsolutions.cl',
    'category': 'Inventory',
    'version': '1.1.1',
    'depends': ['l10n_cl_base',
                ],
    'data': [
        'wizards/wizard_export_inventory_product_time_view.xml',
        'report/product_report_view.xml',
        'report.xml',
    ],
    "external_dependencies": {
        'python': ['dicttoxml',
                   'xmltodict',
                   ]
     },
    'demo': [
    ],
}

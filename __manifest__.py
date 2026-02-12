# -*- coding: utf-8 -*-
{
    'name': "Gestión de Biblioteca",

    'summary': """
        Módulo desarrollado durante la certificación ifct0610 como material evaluable para el bloque tercero.
    """,

    'description': """
        Módulo de biblioteca desarrolado para Odoo 16, conectado con el modulo oficial Contactos de Odoo.
    """,

    'author': "Rafael Rodríguez Calderón",
    'website': "https://ifct0610.xo.je",
    'icon': 'biblioteca/static/description/icon.png',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

}

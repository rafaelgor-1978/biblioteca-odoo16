# -*- coding: utf-8 -*-

from odoo import models, fields


class BibliotecaGenero(models.Model):
    _name = 'biblioteca.genero'
    _description = 'Genero de libros'

    name = fields.Char('Nombre', required=True)
    description = fields.Text('Descripción')

    libro_ids = fields.Many2many(
        comodel_name='biblioteca.libro',
        string='Libros en esta categoría'
    )

    _sql_constraints = [
        (
            'unique_genero_name',
            'UNIQUE(name)',
            '¡Ya existe este género!'
        )
    ]

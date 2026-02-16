# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BibliotecaGenero(models.Model):
    _name = 'biblioteca.genero'
    _description = 'Genero de libros'

    name = fields.Char('Nombre', required=True)
    color = fields.Integer('Color', required=True)  # ← Campo mágico!
    description = fields.Text('Descripción')

    libro_ids = fields.Many2many(
        comodel_name='biblioteca.libro',
        string='Libros en esta categoría'
    )

    # Esto convierte a mayusculas en formulario de genero el campo name.

    @api.onchange('name')
    def _onchange_name_upper(self):
        if self.name:
            self.name = self.name.strip().upper()

    '''
    Utilizamos api.model para pasar a mayusculas el campo name antes de introducirlo en la base de datos o cuando lo modifiquemos, esto
    es necesario pq cuando creamos un genero desde libro la validacion api.onchange no se ejecuta solo lo hace el formulario de genero.
    '''
    @api.model
    def create(self, vals):
        # Esto asegura que si se crea desde Libro (o cualquier sitio), sea mayúscula
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].strip().upper()
        return super(BibliotecaGenero, self).create(vals)

    def write(self, vals):
        # Esto asegura que si se edita, se mantenga en mayúscula
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].strip().upper()
        return super(BibliotecaGenero, self).write(vals)

    _sql_constraints = [
        (
            'unique_genero_name',
            'UNIQUE(name)',
            '¡Ya existe este género!'
        )
    ]

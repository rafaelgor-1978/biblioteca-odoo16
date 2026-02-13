# -*- coding: utf-8 -*-

from odoo import models, fields


class BibliotecaAutor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Datos del autor'

    name = fields.Char(string='Nombre', required=True)
    nacionalidad = fields.Char(string='Nacionalidad')
    biografia = fields.Text(string='Breve biografia')
    imagen = fields.Image(string="Foto del autor",
                          max_width=1920, max_height=1920)
    # cambio libro_autor_ids por libros_ids, me parece mas coherente para comprenderlo
    libros_ids = fields.One2many(
        comodel_name='biblioteca.autor_libro',
        inverse_name='autor_id',
        string='Libros publicados'
    )

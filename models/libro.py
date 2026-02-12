# -*- coding: utf-8 -*-

from odoo import models, fields


class BibliotecaLibro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro de la biblioteca'

    # Campos básicos
    name = fields.Char(string='Título', required=True)
    isbn = fields.Char(string='ISBN', size=13)
    editorial = fields.Char(string='Editorial')
    ano_publicacion = fields.Integer(string='Año de publicación')
    fecha_adquisicion = fields.Date(string='Año adquisicion')
    precio = fields.Float(string='Precio')
    descripcion = fields.Text(string='Breve resumen libro')
    active = fields.Bolean(string='Activo / Inactivo', default=True)
    estado = fields.Selection(
        selection=[
            ('disponible', 'Libro disponible'),
            ('prestado', 'Libro prestado'),
            ('reparacion', 'En reparación'),
            ('perdido', 'Libro perdido'),
        ],
        string='Estado del libro',
        default='disponible',
        required=True
    )

    # IMPORTANTE: Ya NO usamos Many2many
    # Usamos One2many hacia el modelo intermedio
    # Cambio autor_libro_ids por autores_ids, me parece mas coherente para comprenderlo
    autores_ids = fields.One2many(
        comodel_name='biblioteca.autor_libro',
        inverse_name='libro_id',
        string='Autores'
    )

    # Relación con genero (esta sí sigue siendo Many2many simple)
    genero_ids = fields.Many2many(
        comodel_name='biblioteca.genero',
        string='Generos'
    )

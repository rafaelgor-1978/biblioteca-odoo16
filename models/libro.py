# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.fields import Date, Datetime


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
    active = fields.Boolean(string='Activo / Inactivo', default=True)
    imagen = fields.Image(string="Portada del Libro",
                          max_width=1920, max_height=1920)
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
        string='Autores',

    )

    # Relación con genero (esta sí sigue siendo Many2many simple)
    genero_ids = fields.Many2many(
        comodel_name='biblioteca.genero',
        string='Generos'
    )

    @api.constrains('ano_publicacion', 'fecha_adquisicion')
    def _check_fechas(self):
        fecha_actual = Date.today()
        ano_actual = Datetime.now().year
        for record in self:
            if record.ano_publicacion:
                if record.ano_publicacion > ano_actual:
                    raise ValidationError(
                        'El año de publicación es mayor que el año actual')

            if record.fecha_adquisicion:
                if record.fecha_adquisicion >= fecha_actual:
                    raise ValidationError(
                        'La fecha de adquisición es mayor que la fecha actual, ESPABILA!!!')

    _sql_constraints = [
        (
            'unique_isbn',
            'UNIQUE(isbn)',
            '¡Ya existe este este ISBN, debe ser unico!'
        )
    ]

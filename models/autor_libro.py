-*- coding: utf-8 -*-

from odoo import models, fields, api


class BibliotecaAutorLibro(models.Model):
    _name = 'biblioteca.autor_libro'
    _description = 'Relación Autor-Libro con información extra'
    _order = 'libro_id, orden'  # Ordenar por libro y luego por secuencia
    
    # Los dos Many2one que forman la relación
    libro_id = fields.Many2one(
        comodel_name='biblioteca.libro',
        string='Libro',
        required=True,
        ondelete='cascade'  # Si se elimina el libro, se eliminan sus relaciones
    )
    
    autor_id = fields.Many2one(
        comodel_name='biblioteca.autor',
        string='Autor',
        required=True,
        ondelete='cascade'  # Si se elimina el autor, se eliminan sus relaciones
    )

    es_autor_principal = fields.Bolean(
        string='Autor principal',
        default=10,
        help='Marcar si el autor es principal.'
    )

    orden = fields.Integer(
        string='Orden',
        default=10,
        help='Orden en el que se mostraran los autores (1=primer autor, 2=segundo autor, etc.)'
    )

    _sql_constraints = [
        (
            'unique_autor_libro_principal',
            'UNIQUE(libro_id, autor_id)',
            '¡No se puede incluir dos veces al mismo autor!'
        )
    ]
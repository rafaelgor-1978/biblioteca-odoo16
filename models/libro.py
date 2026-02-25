# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.fields import Date, Datetime


class BibliotecaLibro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro de la biblioteca'

    # Campos básicos
    name = fields.Char(string='Título', required=True)
    isbn = fields.Char(string='ISBN', required=True, size=13)
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

    prestamo_ids = fields.One2many(
        comodel_name='biblioteca.prestamo',
        inverse_name='libro_id',
        string='Préstamos'
    )

    prestamos_totales_count = fields.Integer(
        compute='_compute_prestamos_totales')
    prestamos_activos_count = fields.Integer(
        compute='_compute_prestamos_activos')
    prestamos_devueltos_count = fields.Integer(
        compute='_compute_prestamos_devueltos')

    def _compute_prestamos_totales(self):
        for record in self:
            record.prestamos_totales_count = self.env['biblioteca.prestamo'].search_count(
                [('libro_id', '=', record.id)])

    def _compute_prestamos_activos(self):
        for record in self:
            record.prestamos_activos_count = self.env['biblioteca.prestamo'].search_count(
                [('libro_id', '=', record.id), ('estado', '!=', 'devuelto')])

    def _compute_prestamos_devueltos(self):
        for record in self:
            record.prestamos_devueltos_count = self.env['biblioteca.prestamo'].search_count(
                [('libro_id', '=', record.id), ('estado', '=', 'devuelto')])

    def action_filtrar_prestamos(self):
        # 1. Definimos el dominio (las condiciones de filtrado)
        # Ejemplo: campo 'state' es 'draft' y 'priority' es '3' (Alta)
        condiciones = self.env.context.get('estado', False)

        if condiciones:
            if condiciones == 'activo':
                estado = 'devuelto'
                comparador = '!='
                miga = 'Prestamos Activos'

            else:
                estado = condiciones
                comparador = '='
                miga = 'Prestamos Devueltos'
        else:
            estado = ''
            comparador = '!='
            miga = 'Prestamos Totales'

        my_domain = [

            ('estado', comparador, estado),
            ('libro_id', '=', self.id)  # Relacionado con el registro actual
        ]

        # 2. Retornamos la acción de ventana
        return {
            'name': miga,
            'type': 'ir.actions.act_window',
            'res_model': 'biblioteca.prestamo',  # El modelo que quieres listar
            'view_mode': 'tree,form',
            'domain': my_domain,
            # Para que al crear uno nuevo, ya esté vinculado
            'context': {'default_libro_id': self.id},
            'target': 'current',  # 'current' recarga la vista, 'new' abre un pop-up
        }

    def action_libro_prestamo(self):
        """ Abre el formulario de nuevo préstamo con el libro precargado """
        return {
            'name': 'Nuevo Préstamo',
            'type': 'ir.actions.act_window',
            'res_model': 'biblioteca.prestamo',  # El modelo de destino
            'view_mode': 'form',
            # Esto hace que se abra en un popup (ventana modal)
            'target': 'new',
            'context': {
                'default_libro_id': self.id,  # Pasa el ID actual al campo Many2one
            }
        }

    def devolver_desde_libro(self):
        prestamo = self.env['biblioteca.prestamo']
        for record in self:
            prestamo_activo = prestamo.search([
                ('libro_id', '=', record.id),
                ('estado', '=', 'activo')
            ], limit=1)

        if prestamo_activo:
            prestamo_activo.devolver_libro()
        else:
            raise ValidationError(
                'Este libro no tiene prestamos activos')

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

    def write(self, vals):
        if self.env.context.get('saltar_validation'):
            return super().write(vals)

        if 'estado' in vals:
            for record in self:
                estado_anterior = record.estado
                estado_nuevo = vals.get('estado')

                if estado_anterior == 'prestado' and estado_nuevo in ['reparacion', 'perdido', 'disponible']:
                    record.estado = estado_anterior
                    raise ValidationError(
                        "⚠️ Operación no permitida: Un libro que está actualmente 'Prestado' "
                        "no puede pasar a 'Reparación', 'Perdido' o 'Disponible' directamente. "
                        "Primero debe ser devuelto, es decir debe finalizar el prestamos activo."
                    )

                if estado_anterior in ['reparacion', 'perdido', 'disponible'] and estado_nuevo == 'prestado':
                    record.estado = estado_anterior
                    raise ValidationError(
                        "⚠️ Operación no permitida: Para establecer un libro como 'Prestado' "
                        "debe generar un préstamo para este libro."
                    )

        return super().write(vals)

    _sql_constraints = [
        (
            'unique_isbn',
            'UNIQUE(isbn)',
            '¡Ya existe este este ISBN, debe ser unico!'
        )
    ]

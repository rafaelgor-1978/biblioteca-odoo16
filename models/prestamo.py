# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.fields import Date, Datetime


class BibliotecaPrestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = 'Relación entre Contactos(res_partner) y libros'

    name = fields.Char(
        string="Referencia prestamo",
        readonly=True,
        required=True,
        copy=False,
        default='Nuevo'
    )

    libro_id = fields.Many2one(
        comodel_name='biblioteca.libro',
        string='Libro',
        required=True,
        domain=[('estado', '=', 'disponible')],
        ondelete='cascade'  # Si se elimina el libro, se eliminan sus relaciones
    )

    socio_id = fields.Many2one(
        comodel_name='res.partner',
        string='Socio',
        required=True,
        domain=[('es_socio_biblioteca', '=', True)],
        ondelete='cascade'  # Si se elimina el libro, se eliminan sus relaciones
    )

    fecha_prestamo = fields.Date(
        string="Fecha prestamo",
        default=fields.Date.today
    )

    fecha_devolucion_prevista = fields.Date(
        string="Fecha devolución prevista",
        compute='_calcular_devolucion',
        default=fields.Date.today,
        readonly=True
    )
    fecha_devolucion_real = fields.Date(
        string="Fecha devolución real",


    )
    estado = fields.Selection(
        selection=[
            ('activo', 'Prestamo activo'),
            ('devuelto', 'Devuelto'),
            ('retraso', 'Retrasado'),

        ],
        string='Estado del prestamo',
        default='activo',
        required=True
    )

    notas = fields.Text(
        string='Observaciones del préstamo'
    )

    @api.depends('fecha_prestamo')
    def _calcular_devolucion(self):
        for record in self:
            record.fecha_devolucion_prevista = Date.today() + timedelta(days=15)

    @api.constrains('fecha_devolucion_real')
    def _check_fechas(self):
        fecha_actual = Date.today()

        for record in self:
            if record.fecha_devolucion_real:
                if record.fecha_devolucion_real <= fecha_actual:
                    raise ValidationError(
                        'La fecha de de devolucion debe ser mayor que la fecha actual, ESPABILA!!!')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            # 'prestamo.secuencia' debe coincidir con el <code> del XML
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'prestamo.secuencia') or 'Nuevo'
        return super().create(vals)

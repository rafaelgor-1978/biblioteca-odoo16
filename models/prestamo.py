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
        default=lambda self: fields.Date.today() + timedelta(days=15),
        store=True,
        readonly=False
    )
    fecha_devolucion_real = fields.Date(
        string="Fecha devolución real",


    )
    estado = fields.Selection(
        selection=[
            ('activo', 'Prestamo activo'),            
            ('retraso', 'Retrasado'),
            ('devuelto', 'Devuelto'),

        ],
        string='Estado del prestamo',
        default='activo',
        required=True
    )

    notas = fields.Text(
        string='Observaciones'
    )
    # @api.onchange('fecha_prestamo')
    # def _calcular_devolucion(self):
    #     if self.fecha_prestamo:
    #         self.fecha_devolucion_prevista = self.fecha_prestamo + timedelta(days=15)

    @api.depends('fecha_prestamo')
    def _calcular_devolucion(self):
        for record in self:
            if record.fecha_prestamo:
                record.fecha_devolucion_prevista = record.fecha_prestamo + timedelta(days=15)

    @api.constrains('fecha_devolucion_real')
    def _check_fechas(self):
        fecha_actual = Date.today()

        for record in self:
            if record.fecha_devolucion_real:
                if record.fecha_devolucion_real < fecha_actual:
                    raise ValidationError(
                        'La fecha de de devolucion debe ser mayor que la fecha actual, ESPABILA!!!')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            # 'prestamo.secuencia' debe coincidir con el <code> del XML
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'prestamo.secuencia') or 'Nuevo'          
        
        prestamos = super().create(vals)

        for prestamo in prestamos:
            prestamo.libro_id.estado = 'prestado'
        return prestamos
    
    @api.model
    def _cron_actualizar_retrasados(self):
        """
        Ejecutado por Odoo automáticamente cada día.
        Busca préstamos activos con fecha vencida y los marca como retrasado.
        """

        print("--- INICIANDO CRON DE PRESTAMOS ---")

        hoy = fields.Date.today()   # Con () porque estamos DENTRO de un método:
                                    # queremos el valor de hoy en este momento exacto.
                                    # Aquí no hay ningún bug: el código se ejecuta
                                    # cada vez que el cron corre.

        prestamos_retrasados = self.search([
            ('estado', '=',  'activo'),
            ('fecha_devolucion_prevista', '<', hoy)
        ])

        # write() en recordset → una sola consulta SQL para todos los registros
        prestamos_retrasados.write({'estado': 'retraso'})
    
    def devolver_libro(self):
        for record in self:
            if record.estado == 'devuelto':
                raise ValidationError("El estado del prestamo ya es devuelto!!!")
            
            record.fecha_devolucion_real = fields.Date.today()
            record.estado ='devuelto'
            record.libro_id.estado = 'disponible'
            
    def boton_fantasma(self):
        # Este método no hace nada, solo sirve para que el botón XML sea válido
        pass

    def activar_prestamo(self):
        for record in self:
            hoy = fields.Date.today()
            if record.fecha_devolucion_prevista:
                if record.fecha_devolucion_prevista < hoy:
                    record.estado = 'retraso'
                    record.libro_id.estado = 'prestado'
                else:
                    record.estado = 'activo'
                    record.libro_id.estado = 'prestado'


            



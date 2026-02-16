
from odoo import models, fields


class ResPartner(models.Model):
    # ¡IMPORTANTE! Usamos _inherit sin _name
    _inherit = 'res.partner'

    # Añadimos nuestros campos personalizados
    es_socio_biblioteca = fields.Boolean(
        string='Es Socio de Biblioteca',
        default=False,
        help='Marca si este contacto es socio de la biblioteca'
    )

    prestamo_ids = fields.One2many(
        comodel_name='biblioteca.prestamo',
        inverse_name='socio_id',
        string='Préstamos'
    )

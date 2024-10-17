# -*- coding: utf-8 -*

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    integer_range = fields.Integer(string='Integer Range',
                                   help='helps the user to pick an integer value using the slider')

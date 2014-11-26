# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
_logger = logging.getLogger(__name__)

from openerp import fields, models


class base_format(models.Model):
    """ This model associates a format and 3 product templates."""
    _inherit = 'base.format'

    product_black_white = fields.Many2one(
        'product.template', string='Black and White'
    )
    product_color = fields.Many2one(
        'product.template', string='Color'
    )
    product_mixed = fields.Many2one(
        'product.template', string='Mixed'
    )

# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
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
from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class product_template(models.Model):
    """ Associates a format to a product. """
    _inherit = 'product.template'
    allowed_format_ids = fields.Many2many(
        'base.format',
        related='order_destination.format_ids',
    )

    @api.onchange('order_destination')
    def onchange_destination(self):
        """  Reset the value of the format field when the order destination is
            changed.
        """
        self.format = False

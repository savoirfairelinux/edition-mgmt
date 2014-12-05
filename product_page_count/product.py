# -*- encoding: utf-8 -*-
# #############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2014 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# #############################################################################

import logging
from openerp.osv import fields, orm
from openerp import api

_logger = logging.getLogger(__name__)


class product_product(orm.Model):
    """
    Add page_count field.
    """
    _inherit = 'product.template'

    _columns = {
        'page_count': fields.integer('Total number of pages', default=0),
        'color_page_count': fields.integer('Number of pages in color', default=0),
    }

    @staticmethod
    def _compute_pair_page_count(vals):
        page_count = vals.get('page_count')
        if page_count and page_count % 2:
            vals['page_count'] = page_count + 1

        return vals

    @api.model
    def create(self, vals, context=None):
        return super(product_product, self).create(
            self._compute_pair_page_count(vals),
            context=context
        )

    @api.multi
    def write(self, vals, context=None):
        return super(product_product, self).write(
            self._compute_pair_page_count(vals),
            context=context
        )

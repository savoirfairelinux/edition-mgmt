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
"""This module subclass the product.template."""

import logging
from openerp.osv import fields, orm
from openerp import api
from openerp.tools.translate import _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class product_product(orm.Model):

    """
    Add page_count and color_page_count fields.

    The field are used to save the number of normal page
    in a book and the number of colored page in a book.
    """

    _inherit = 'product.template'

    _columns = {
        'page_count': fields.integer('Total number of pages', default=2),
        'color_page_count': fields.integer('Number of pages in color',
                                           default=0),
    }

    @api.constrains('page_count')
    def _page_count_positive(self):
        """
        page_count constraint.

        This function constrains the page_count field to a value
        higher than 0. Value below 1 are invalid.
        """
        for record in self:
            if record.page_count < 1:
                raise ValidationError(_("The number of pages has "
                                      "to be more than zero (0)."))

    @api.constrains('color_page_count')
    def _color_page_count_positive(self):
        """
        color_page_count constraint.

        This function constrains the color_page_count field to a
        positive value.
        """
        for record in self:
            if record.color_page_count < 0:
                raise ValidationError(_("The number of color pages has "
                                      "be equal to or above zero (0)."))

    @staticmethod
    def _compute_pair_page_count(vals):
        """
        Recompute the page_count value.

        It recompute the page_count value to a multiple of two.
        Pages usually two sides which is why the quantity of page
        can't be a odd number. This function make sure we don't save
        an odd number of pages in the database.
        """
        page_count = vals.get('page_count')
        if page_count and page_count % 2:
            vals['page_count'] = page_count + 1

        return vals

    @api.model
    def create(self, vals, context=None):
        """
        Override the model create method.

        The create method call the _compute_pair_page_count
        method before the value is saved in the database. It
        ensure that the number of page is a multiple of two.
        """
        return super(product_product, self).create(
            self._compute_pair_page_count(vals),
            context=context
        )

    @api.multi
    def write(self, vals, context=None):
        """
        Override the model write method.

        The write method call the _compute_pair_page_count
        method before the value is saved in the database. It
        ensure that the number of page is a multiple of two.
        """
        return super(product_product, self).write(
            self._compute_pair_page_count(vals),
            context=context
        )

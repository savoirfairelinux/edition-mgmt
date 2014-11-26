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


_logger = logging.getLogger(__name__)


class product_template(orm.Model):
    """Add spine field and the way to calculate it"""
    _inherit = 'product.template'

    @staticmethod
    def calculate_spine(number_pages=0,
                        paper_thickness=0.0,
                        cover_thickness=0.0):
        """Calculate the spine according to the equation:
        (paper_thickness * number_pages) + cover_thickness
        :param number_pages: int
        :param paper_thickness: float (in mm)
        :param cover_thickness: float (in mm)
        :return: float (in cm)
        """
        pages = number_pages * paper_thickness
        total = pages + cover_thickness
        return total / 10

    _columns = {
        'spine': fields.float('Spine (cm)', digits=(8, 4))
    }

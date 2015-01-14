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

from openerp.tests import common


class test_product_template(common.TransactionCase):
    def setUp(self):
        super(test_product_template, self).setUp()
        self.product_template_model = self.env['product.template']

    def test_calculate_spine(self):
        """Test if the maths are right here."""
        product_template = self.product_template_model.create(
            {'name': 't_name'}
        )

        # more than one set of values is test to avoid to
        # have a special case that would fit the case by chance.

        spine = product_template.calculate_spine(
            number_pages=290,
            paper_thickness=0.058,
            cover_thickness=0.6
        )
        self.assertAlmostEqual(spine, 1.742)

        spine = product_template.calculate_spine(
            number_pages=80,
            paper_thickness=0.058,
            cover_thickness=0.6
        )
        self.assertAlmostEqual(spine, 0.524)

        spine = product_template.calculate_spine(
            number_pages=160,
            paper_thickness=0.0645,
            cover_thickness=0.69
        )
        self.assertAlmostEqual(spine, 1.101)

        spine = product_template.calculate_spine(
            number_pages=500,
            paper_thickness=0.043,
            cover_thickness=0.6
        )
        self.assertAlmostEqual(spine, 2.21)

# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
        self.publication_mgmt_model = self.env['publication.management']
        self.product_template_model = self.env['product.template']
        user = self.env['res.users'].browse(self.uid)
        model_data_model = self.env['ir.model.data']
        main_partner = model_data_model.get_object(
            'base',
            'main_partner',
        )

        # user has to have a company to save a product.template
        # due to dependencies.
        user.write({'parent_id': main_partner.id})
        self.publication = self.publication_mgmt_model.create({
            'title': 'p_title', 'author': 'p_author',
        })

    def test_public_categ_id_has_publication_categ(self):
        """The version should have the public_categ_id in its product public
        categories.
        """
        template = self.product_template_model.create({
            'name': 't_name', 'publication': self.publication.id
        })
        self.assertIn(
            self.publication.public_category_id,
            template.public_categ_ids
        )

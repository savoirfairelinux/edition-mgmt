# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
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


class test_publication_management(common.TransactionCase):
    def setUp(self):
        super(test_publication_management, self).setUp()
        self.publication_mgmt_model = self.env['publication.management']
        self.product_category_model = self.env['product.category']
        self.model_data_model = self.env['ir.model.data']
        self.publication_categ = self.model_data_model.get_object(
            'publication_management_product_category',
            'publication_management_publication_category',
        )
        self.category_name = self.publication_categ.name

    def test_product_category_publications_exists(self):
        """A product.category "Publication" exists.
        It has category 'All' as parent.
        """
        self.assertEqual(self.publication_categ.parent_id.name, 'All')

    def test_create_got_category(self):
        """When a new publication.management record is created,
        a product.category should be created as well
        The relation is set through
        publication_management.product_category_id field
        The new category has to have the same name than
        publication_management.title and have product.category "publication"
        as parent.
        """
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        category = publication.product_category_id
        # Checking if the category exists
        self.assertTrue(category)

    def test_create_got_category_publication_categ_as_parent(self):
        """the new category has to have product.category "publication"
        as parent.
        """
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        category = publication.product_category_id
        # the category as publications category as parent
        self.assertEqual(category.parent_id, self.publication_categ)

    def test_create_got_category_same_name_as_publication(self):
        """The new category has to have the same name than
        publication_management.title
        """
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        category = publication.product_category_id
        # the name of the category is the same than the name of the
        # publication it is related to.
        self.assertEqual(category.name, publication.title)

    def test_write(self):
        """When a publication.management record is saved, the
        product.category related to it should be updated according to the
        changes.
        ie: the name of the category is the same than the publication.title
        even after an update
        """
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        category = publication.product_category_id
        # Checking the category got the same name than the publication
        self.assertEqual(category.name, publication.title)
        publication.write({'title': 'pp_test'})
        # Even after a save.
        self.assertEqual(category.name, publication.title)

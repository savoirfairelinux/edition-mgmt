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
        self.model_data_model = self.env['ir.model.data']

    def test_create_got_category(self):
        """When a new publication.management record is created,
        a product.public.category should be created as well
        The relation is set through
        publication_management.public_category_id field
        """
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        public_category_id = publication.public_category_id
        # Checking if the category exists
        self.assertTrue(public_category_id)

    def test_category_got_partner(self):
        """The public category got the parent of current partner as partner.
        """
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        # Checking if the category exists
        self.assertEqual(
            publication.public_category_id.partner_id,
            publication.partner_id
        )

    def test_create_got_category_publication_categ_as_no_parent(self):
        """the new category has no parent."""
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        public_category_id = publication.public_category_id
        # the category as publications category as parent
        self.assertFalse(public_category_id.parent_id)

    def test_create_got_category_same_name_as_publication(self):
        """The new category has to have the same name than
        publication_management.title
        """
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        public_category_id = publication.public_category_id
        # the name of the category is the same than the name of the
        # publication it is related to.
        self.assertEqual(public_category_id.name, publication.title)

    def test_write(self):
        """When a publication.management record is saved, the
        product.public.category related to it should be updated according to
        the changes.
        ie: the name of the category is the same than the publication.title
        even after an update
        """
        publication = self.publication_mgmt_model.create(
            {'title': 'p_test', 'author': 'p_author'}
        )
        public_category_id = publication.public_category_id
        # Checking the category got the same name than the publication
        self.assertEqual(public_category_id.name, publication.title)
        publication.write({'title': 'pp_test'})
        # Even after a save.
        self.assertEqual(public_category_id.name, publication.title)

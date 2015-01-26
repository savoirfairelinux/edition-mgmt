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

from openerp.exceptions import except_orm
from openerp import api
from openerp.tests import common


class test_base_format(common.TransactionCase):
    def setUp(self):
        super(test_base_format, self).setUp()
        self.product_template_model = self.env['product.template']
        self.partner_obj = self.env['res.partner']
        self.user_obj = self.env['res.users']

    def test_save_create_extension_empty_vals(self):
        """save_create_extension works even with an empty dict.
        """
        vals = self.product_template_model.save_create_extension({})
        self.assertNotEqual(vals, {})

    def test_save_create_extension_raise(self):
        """Save_create_extension raises except_orm if the partner doesn't have
        a parent.
        """
        # As the default partner is the admin, and the admin doesn't have
        # any parent, we test with it.
        self.assertRaises(
            except_orm,
            self.product_template_model.save_create_extension,
            {'publication': 't_publication'}
        )

    def test_save_create_extention_set_unique_partner_id(self):
        """save_create_extension set unique_partner_id if publication
        in vals.
        """
        parent = self.partner_obj.create(
            {'name': 't_parent'}
        )
        partner = self.partner_obj.create(
            {
                'name': 't_partner',
                'parent_id': parent.id
            }
        )
        user = self.user_obj.create(
            {
                'login': 't_user',
                'partner_id': partner.id
            }
        )
        user_env = api.Environment(self.cr, user.id, {})
        templates = user_env['product.template']

        vals = templates.save_create_extension(
            {'publication': 't_publication'}
        )
        self.assertEqual(vals['unique_partner_id'], parent.id)




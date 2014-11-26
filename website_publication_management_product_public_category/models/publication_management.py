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


class publication_management(orm.Model):
    """Publication Management with product_category_id"""
    _inherit = 'publication.management'

    @api.model
    def create(self, vals):
        """Overcharge of the method to add the relation with a product.category
        :param vals: dict
        :return: record
        """
        # Running the super before to be sure to have all the update for
        # the record
        rec = super(publication_management, self).create(vals)

        # Creating the new product.category with the same name as the title
        # of the record.
        product_public_categ_model = self.env['product.public.category']
        public_categ = product_public_categ_model.create({
            'name': rec.title,
            'partner_id': rec.partner_id.id,
        })

        # And relate it to the record
        rec.write({'public_category_id': public_categ.id})
        return rec

    @api.multi
    def write(self, vals):
        """Overcharge of the method to sync the name of the category with
        the title of the record.
        :param vals: dict
        :return: record
        """
        # To be sure the record details are update through the RMO
        super(publication_management, self).write(vals)
        # Blind update.
        self.public_category_id.write({'name': self.title})
        return True

    _columns = {
        'public_category_id': fields.many2one(
            'product.public.category',
            string='Public Category'
        )
    }

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
_logger.setLevel(logging.DEBUG)


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
        _logger.debug('create')
        rec = super(publication_management, self).create(vals)

        # Getting the parent category record
        model_data = self.env['ir.model.data']
        publication_categ = model_data.get_object(
            'publication_management_product_category',
            'publication_management_publication_category',
        )

        # Creating the new product.category with the same name as the title
        # of the record.
        product_categ_model = self.env['product.category']
        categ = product_categ_model.create({
            'name': rec.title, 'parent_id': publication_categ.id
        })

        # And relate it to the record
        rec.write({'product_category_id': categ.id})
        return rec

    @api.model
    def write(self, vals):
        """Overcharge of the method to sync the name of the category with
        the title of the record.
        :param vals: dict
        :return: record
        """
        # To be sure the record details are update through the RMO
        super(publication_management, self).write(vals)
        # Blind update.
        self.product_category_id.write({'name': self.title})
        return self

    _columns = {
        'product_category_id': fields.many2one(
            'product.category',
            string='Product Category'
        )
    }

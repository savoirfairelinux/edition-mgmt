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


class product_template(orm.Model):
    """Product template update of the categories"""
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        rec = super(product_template, self).create(vals)
        publication = rec.publication
        if publication:
            rec.write(
                {'public_categ_ids': [(4, publication.public_category_id.id)]}
            )
        return rec

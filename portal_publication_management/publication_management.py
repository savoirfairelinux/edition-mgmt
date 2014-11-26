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
from openerp import tools
import ast

_logger = logging.getLogger(__name__)


class portal_publication_management(orm.Model):
    """
    Portal Publication Management table
    """
    _inherit = 'publication.management'

    _columns = {
        'publication_rule': fields.function(
            lambda self, *a, **kw: 1,  # placeholder. Not used further anyway
            string="Search rule",
            fnct_search=lambda self, *a, **kw: self._search_rule(*a, **kw),
        )
    }

    def _search_rule(self, cr, uid, ids, name, args, context=None):
        """ odoo code to find ids you want to display -> return_ids """
        user = self.pool.get('res.users').browse(cr, uid, uid)
        return [('partner_id', '=', user.partner_id.parent_id.id)]

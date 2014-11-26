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
from openerp.exceptions import except_orm
from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp import api

_logger = logging.getLogger(__name__)


class product_template(orm.Model):
    """ Overcharge with Sobook specifics details. """
    _inherit = 'product.template'
    __version_state = 'proposition_draft'

    def save_create_extension(self, cr, uid, vals):
        """  Test and updates that are needed at create and save step. """
        # Checking if the product_template has a publication linked to it.
        # if so that means it is version actually, and a version
        # has to have a partner linked to it.
        if vals.get('publication', None):
            user = self.pool.get('res.users').browse(cr, uid, uid)
            if not vals.get('unique_partner_id'):
                if not user.parent_id:
                    raise except_orm(
                        _('Error!'), _('You need to be linked to a company.')
                    )
                vals['unique_partner_id'] = user.parent_id.id

        # if the version name is set, to avoid to have to overcharge all the
        # view with a product template, the value is copied into name.
        version_name = vals.get('version_name', '')
        if version_name:
            vals['name'] = version_name
        # we use get here as the value state might not be already set
        # at this stage, in the case of demo data for example.
        vals['name_switch'] = is_a_version(vals.get('state', ''))
        return vals

    def write(self, cr, uid, ids, vals, context=None):
        """  overcharges the write method to extend with our values. """
        return super(product_template, self).write(
            cr, uid, ids,
            self.save_create_extension(cr, uid, vals),
            context=context
        )

    def create(self, cr, uid, vals, context=None):
        """  overcharges the create method to extend with our values. """
        vals['state'] = vals.get('state', self.__version_state)
        active_id = context.get('active_id')
        active_model = context.get('active_model')
        if active_id and active_model == 'publication.management':
            vals['publication'] = active_id
            # a version has no price.
            vals['list_price'] = 0.0
        return super(product_template, self).create(
            cr, uid,
            self.save_create_extension(cr, uid, vals),
            context=context
        )

    @api.onchange('state')
    def onchange_destination(self):
        """  Reset the value of the format field when the order destination is
            changed.
        """
        self.name_switch = is_a_version(self.state)

    _columns = {
        # version_name is a placeholder of name field for versions.
        # name field is not changed to allow us to keep the translation
        # for regular product for instance.
        'version_name': fields.char(
            'Name', translate=False, select=True
        ),
        'name_switch': fields.boolean(),
        'publication': fields.many2one('publication.management',
                                       string='Publication'),

        # I am not sure here the state option should not be a type instead
        'state': fields.selection(
            [
                ('', ''),
                ('draft', 'In Development'),
                ('sellable', 'Normal'),
                ('end', 'End of Lifecycle'),
                ('obsolete', 'Obsolete'),
                ('option', 'Option'),
                ('proposition', 'Proposition'),
                ('proposition_draft', 'Draft Of Proposition'),
                ('proposition_canceled', 'Proposition Canceled'),
                ('orderable', 'Orderable'),
                ('Version', 'Version')
            ],
            'Status'
        ),

    }

    _defaults = {
        'type': 'service',
        'state': __version_state,
    }


def is_a_version(state):
    version_states = (
        'proposition',
        'proposition_draft',
        'proposition_canceled',
        'orderable',
        'Version',
    )
    return state in version_states


class publication_management(orm.Model):
    _inherit = 'publication.management'

    @api.multi
    def _count_version(self, field_name, arg):
        return {pm.id: len(pm.version) for pm in self}

    _columns = {
        'nb_version': fields.function(_count_version, string="Nb Version",
                                      type='integer', store=False),

        'version': fields.one2many('product.template', 'publication',
                                   string='Versions'),
    }

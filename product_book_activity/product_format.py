# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class product_template(models.Model):
    """ Associates a format to a product. """
    _inherit = 'product.template'
    allowed_format_ids = fields.Many2many(
        'base.format',
        related='order_destination.format_ids',
    )
    impression_types = fields.Selection(
        [
            ('monochrome', 'Black & White'),
            ('color', 'Color'),
            ('combined', 'Combined (Black & White + color)'),
        ],
        default='monochrome',
        string='Impressions',
    )

    def format_in_allowed_format_ids(self, vals):
        """Run tests against allowed formats to be sure the format in vals
        is valid for the destination.

        :param vals: values describing the record
        :raise ValidationError: if the format is not in the allowed formats.
        :return: vals (unchanged)
        """
        _logger.debug('format_in_allowed_format_ids')
        _logger.debug('vals: {}'.format(vals))
        format_id = vals.get('format', self.format.id)
        vals_allowed_format_ids = vals.get('allowed_format_ids', False)

        if vals_allowed_format_ids:
            allowed_format_ids = vals_allowed_format_ids[0][-1]
        else:
            allowed_format_ids = [f.id for f in self.allowed_format_ids]

        if format_id:
            _logger.debug(
                'format_: {}, allowed_format_ids: {}, valid? {}'.format(
                    format_id, allowed_format_ids,
                    format_id in allowed_format_ids
                )
            )
            if not format_id in allowed_format_ids:
                raise ValidationError(
                    _(
                        'The selected format is not valid for your destination.'
                        ' Please update the format or the destination.'
                    )
                )
        return vals

    @api.multi
    def write(self, vals):
        """Overcharge the method to test the format of the record.

        :param vals: unchanged
        :return: unchanged
        """
        return super(product_template, self).write(
            self.format_in_allowed_format_ids(vals)
        )

    @api.model
    def create(self, vals):
        """Overcharge the method to test the format of the record.

        :param vals: unchanged
        :return: unchanged
        """
        return super(product_template, self).create(
            self.format_in_allowed_format_ids(vals)
        )

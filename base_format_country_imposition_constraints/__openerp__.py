# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
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
##############################################################################

{
    'name': 'Base Format Country Imposition Constraints',
    'version': '0.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Edition',
    'summary': 'Add field to specify constraints for imposition (n-ups)',
    'description': """
Base Format Country Imposition Constraints
==========================================
This module adds fields to specify the height and width to switch between
2up and 4up.
The specification are related country.

Contributors
------------

* Jordi Riera (jordi.riera@savoirfairelinux.com)
* Bruno JOLIVEAU (bruno.joliveau@savoirfairelinux.com)

More information
----------------

Module developed and tested with Odoo version 8.0
For questions, please contact our support services (support@savoirfairelinux.com)

""",
    'depends': [
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'res_country_view.xml',
    ],
    'installable': True,
}

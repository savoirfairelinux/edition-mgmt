# -*- encoding: utf-8 -*-

from openerp.tests import common
from openerp.exceptions import ValidationError


no_page_error = 'The number of page has to be more than zero (0).'
neg_col_page = 'The number of color page has be equal to or above zero (0).'


class TestModelAction(common.TransactionCase):

    def test_create_product_with_page_count(self):

        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 1,
        })

        self.assertEqual(record.page_count, 2)

        record.write({"page_count": 2})
        self.assertEqual(record.page_count, 2)

        record.write({"page_count": 3})
        self.assertEqual(record.page_count, 4)

        record.write({"page_count": 4})
        self.assertEqual(record.page_count, 4)

        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 2,
        })

        self.assertEqual(record.page_count, 2)


        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 3,
        })

        self.assertEqual(record.page_count, 4)

        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 4,
        })

        self.assertEqual(record.page_count, 4)

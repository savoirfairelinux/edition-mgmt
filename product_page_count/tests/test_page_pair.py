# -*- encoding: utf-8 -*-
"""
Tests product.template.

Check if page count is saved as pair.
"""

from openerp.tests import common


class TestModelAction(common.TransactionCase):

    """Test Case."""

    def test_create_product_page_count_pair(self):
        """
        Test page count value.

        Test if page count are always saved as a
        product of two higher than the number entered.

        For example:

        page_count == 1 => 2
        page_count == 2 => 2
        page_count == 3 => 4
        ...

        """
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

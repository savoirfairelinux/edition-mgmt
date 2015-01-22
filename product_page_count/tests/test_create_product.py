# -*- encoding: utf-8 -*-
"""
Test product.template creation.

Check for multiple input for page_count and color_page_count.
"""

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestModelAction(common.TransactionCase):

    """TestCase."""

    def test_create_product_without_page(self):
        """
        Test product template created without page count.

        Checks if undefined values are going to raise errors.
        """
        with self.assertRaises(ValidationError):
            self.env['product.template'].create({
                "name": "Table",
            })

    def test_create_product_with_page_count_negative(self):
        """
        Test negative page count.

        Page count must be equal to 1 or higher.
        """
        with self.assertRaises(ValidationError):
            self.env['product.template'].create({
                "name": "Table",
                "page_count": -1
            })

    def test_create_product_with_page_count_null(self):
        """
        Test null page count.

        Page count must be equal to 1 or higher.
        """
        with self.assertRaises(ValidationError):
            self.env['product.template'].create({
                "name": "Table",
                "page_count": 0
            })

    def test_create_product_with_page_count_positive(self):
        """
        Test positive page count.

        Page count must be equal to 1 or higher.
        """
        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 1
        })

        self.assertGreater(record.page_count, 0)

    def test_create_product_with_color_page_negative(self):
        """
        Test negative color page count.

        Color page count must be equal to 0 or higher.
        """
        with self.assertRaises(ValidationError):
            self.env['product.template'].create({
                "name": "Table",
                "page_count": 1,
                "color_page_count": -1,
            })

    def test_create_product_with_color_page_null(self):
        """
        Test null color page count.

        Color page count must be equal to 0 or higher.
        """
        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 1,
            "color_page_count": 0,
        })

        self.assertEqual(record.color_page_count, 0)

    def test_create_product_with_color_page_positive(self):
        """
        Test positive color page count.

        Color page count must be equal to 0 or higher.
        """
        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 1,
            "color_page_count": 1,
        })

        self.assertGreater(record.color_page_count, 0)

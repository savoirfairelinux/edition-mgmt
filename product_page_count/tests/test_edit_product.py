# -*- encoding: utf-8 -*-
"""
Test product.template.

Test edition of page_count and color_page_count of
product.template objects.
"""

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestModelAction(common.TransactionCase):
    """Test product.template page count."""

    def setUp(self):
        """Create valid product.template record."""
        self.product = self.env['product.template'].create({
            "name": "Table",
            "page_count": 1,
            "color_page_count": 1,
        })

    def test_edit_product_page_count_none(self):
        """Set page count to None.

        It shouldn't be possible to set an undefined page_count to
        a product.template object.
        """
        with self.assertRaises(ValidationError):
            self.product.write({"page_count": None})

    def test_edit_product_with_page_count_negative(self):
        """Set page count to a negative number.

        It shouldn't be possible to set a negative
        page_count to a product.template object.
        """
        with self.assertRaises(ValidationError):
            self.product.write({"page_count": -1})

    def test_edit_product_with_page_count_null(self):
        """Set page count to 0.

        It shouldn't be possible to set a page_count
        to 0 for a product.template object.
        """
        with self.assertRaises(ValidationError):
            self.product.write({"page_count": 0})

    def test_edit_product_with_page_count_positive(self):
        """Set page count to a positive number.

        It should be possible to set the page_count
        to a positive number.
        """
        self.product.write({"page_count": 1000})
        self.assertGreater(self.product.page_count, 0)

    def test_edit_product_with_color_page_count_negative(self):
        """Set a negative color page count.

        It shouldn't be possible to set a negative color_page_count
        to a product.template object.
        """
        with self.assertRaises(ValidationError):
            self.product.write({"color_page_count": -1})

    def test_edit_product_with_color_page_count_null(self):
        """Set color page count to 0.

        It should be possible to set the color_page_count
        to 0 for a product.template object.
        """
        self.product.write({"color_page_count": 0})
        self.assertEqual(self.product.color_page_count, 0)

    def test_edit_product_with_color_page_count_positive(self):
        """Set color page count to a positive number.

        It should be possible to set the color_page_count
        to any positive number for a product.template object.
        """
        self.product.write({"color_page_count": 100})
        self.assertEqual(self.product.color_page_count, 100)

        self.product.write({"color_page_count": 101})
        self.assertEqual(self.product.color_page_count, 100)

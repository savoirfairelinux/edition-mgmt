# -*- encoding: utf-8 -*-

from openerp.tests import common
from openerp.exceptions import ValidationError


no_page_error = 'The number of page has to be more than zero (0).'
neg_col_page = 'The number of color page has be equal to or above zero (0).'


class TestModelAction(common.TransactionCase):

    def test_create_product_without_page(self):

        try:
            self.env['product.template'].create({
                "name": "Table",
            })
            self.assertEqual(True, False)
        except ValidationError as m:
            self.assertEqual(m.value, no_page_error)

    def test_create_product_with_page_count(self):

        try:
            self.env['product.template'].create({
                "name": "Table",
                "page_count": 0
            })
            self.assertEqual(True, False)
        except ValidationError as m:
            self.assertEqual(m.value, no_page_error)

        try:
            self.env['product.template'].create({
                "name": "Table",
                "page_count": 0
            })
            self.assertEqual(True, False)
        except ValidationError as m:
            self.assertEqual(m.value, no_page_error)

        try:
            self.env['product.template'].create({
                "name": "Table",
                "page_count": -1
            })
            self.assertEqual(True, False)
        except ValidationError as m:
            self.assertEqual(m.value, no_page_error)

        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 1
        })

        self.assertGreater(record.page_count, 0)

    def test_create_product_with_color_page(self):
        try:
            self.env['product.template'].create({
                "name": "Table",
                "page_count": 1,
                "color_page_count": -1,
            })
            self.assertEqual(True, False)
        except ValidationError as m:
            self.assertEqual(m.value, neg_col_page)

        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 1,
            "color_page_count": 0,
        })

        self.assertEqual(record.color_page_count, 0)

        record = self.env['product.template'].create({
            "name": "Table",
            "page_count": 1,
            "color_page_count": 1,
        })

        self.assertGreater(record.color_page_count, 0)

    def test_create_product_with_page_count_negative(self):
        try:
            self.env['product.template'].create({
                "name": "Table",
                "page_count": -1,
                "color_page_count": 1,
            })
            self.assertEqual(True, False)
        except ValidationError as m:
            self.assertEqual(m.value, no_page_error)

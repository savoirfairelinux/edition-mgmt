# -*- encoding: utf-8 -*-

from openerp.tests import common
from openerp.exceptions import ValidationError


class TestProductTemplate(common.TransactionCase):
    """Test Case."""

    def setUp(self):
        super(TestProductTemplate, self).setUp()
        product_template_obj = self.env['product.template']

        # need to create format to link them to country afterwards
        format_obj = self.env['base.format']
        self.format1 = format_obj.create({'name': 't_format1'})
        self.format2 = format_obj.create({'name': 't_format2'})

        country_obj = self.env['res.country']
        self.country1 = country_obj.browse(1)
        self.country1.write(
            {
                'format_ids': [(6, 0, [self.format1.id])],
                'allow_for_destination': True
            }
        )

        self.country2 = country_obj.browse(2)
        self.country2.write(
            {
                'format_ids': [(6, 0, [self.format2.id])],
                'allow_for_destination': True
            }
        )
        self.product_template = product_template_obj.create(
            {
                'name': 't_name',
                # To be sure no country is selected here.
                'order_destination': False
            }
        )

    def test_format_in_allowed_format_ids_depend_on_country(self):
        """The format we can select in allowed_format_ids depends on the
        country selected in order_destination.
        """
        self.product_template.order_destination = self.country1.id
        self.assertIn(
            self.format1,
            self.product_template.allowed_format_ids
        )
        self.assertNotIn(
            self.format2,
            self.product_template.allowed_format_ids
        )

        # If the order_destination is set to another country,
        # we don't have access to the same formats now.
        self.product_template.order_destination = self.country2.id
        self.assertIn(
            self.format2,
            self.product_template.allowed_format_ids
        )
        self.assertNotIn(
            self.format1,
            self.product_template.allowed_format_ids
        )

    def test_format_in_allowed_format_ids_or_validationerror(self):
        """Test if the given format is not in the format of the
        destination, the ValidationError is raised.
        """
        self.product_template.order_destination = self.country1.id
        self.product_template.format = \
            self.product_template.allowed_format_ids[0].id
        self.assertEqual(
            self.product_template.format.id,
            self.product_template.allowed_format_ids[0].id
        )
        self.product_template.order_destination = self.country2.id

        with self.assertRaises(ValidationError):
            self.product_template.format = self.format1.id

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import SavepointCase


@tagged("post_install", "-at_install")
class TestSaleOrderPartnerRestrict(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.main_company = cls.env.ref("base.main_company")
        cls.second_company = cls.env["res.company"].create({"name": "Second Company"})

        cls.partner_model = cls.env["res.partner"]

        cls.partner_parent = cls.partner_model.create(
            {"name": "Partner Parent", "type": "contact"}
        )
        cls.partner_child = cls.partner_model.create(
            {
                "name": "Partner Child",
                "type": "contact",
                "parent_id": cls.partner_parent.id,
            }
        )
        cls.partner_delivery_address = cls.partner_model.create(
            {
                "name": "Partner delivery addresses",
                "type": "delivery",
                "parent_id": cls.partner_parent.id,
            }
        )
        cls.partner_diff_company = cls.partner_model.create(
            {
                "name": "Partner Different Company",
                "type": "contact",
                "company_id": cls.second_company.id,
            }
        )
        cls.partner_delivery = cls.partner_model.create(
            {
                "name": "Partner Delivery",
                "type": "other",
                "parent_id": cls.partner_parent.id,
            }
        )

    def _create_sale_order(self, partner):
        so = self.env["sale.order"].create(
            {"partner_id": partner.id, "name": "/", "company_id": self.main_company.id}
        )
        return so

    def test_sale_order_partner_restrict_option_all(self):
        """Test for a restriction with the "all" option"""
        self.main_company.sale_order_partner_restrict = "all"

        self.assertTrue(
            self._create_sale_order(self.partner_parent),
            "Parent and contact type partner " "should be available on 'all' option",
        )

        self.assertTrue(
            self._create_sale_order(self.partner_child),
            "Child and contact type partner " "should be available in 'all' option",
        )

        # Partner from another company
        # shouldn't be available on this company (option 'all')
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_diff_company)

        self.assertTrue(
            self._create_sale_order(self.partner_delivery),
            "Child and other type partner " "should be available in 'all' option",
        )

    def test_sale_order_partner_restrict_option_only_parents(self):
        """Test for a restriction with the "only_parents" option"""

        self.main_company.sale_order_partner_restrict = "only_parents"

        self.assertTrue(
            self._create_sale_order(self.partner_parent),
            "Parent and contact type partner "
            "should be available in 'only_parents' option",
        )

        # Child and contact type partner shouldn't be available in 'only_parents' option
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_child)

        # Partner from another company
        # shouldn't be available on this company (option 'only_parents')
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_diff_company)

        # Child and other type partner
        # shouldn't be available in 'only_parents' option
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_delivery)

    def test_sale_order_partner_restrict_option_parents_and_contacts(self):
        """Test for a restriction with the "parents_and_contacts" option"""

        self.main_company.sale_order_partner_restrict = "parents_and_contacts"

        self.assertTrue(
            self._create_sale_order(self.partner_parent),
            "Parent and contact type partner "
            "should be available in 'parents_and_contacts' option",
        )

        self.assertTrue(
            self._create_sale_order(self.partner_child),
            "Child and contact type partner "
            "should be available in 'parents_and_contacts' option",
        )

        # Partner from another company
        # shouldn't be available on this company (option 'parents_and_contacts')
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_diff_company)

        # Child and other type partner
        # shouldn't be available in 'parents_and_contacts' option
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_delivery)

    def test_sale_order_partner_restrict_option_only_contacts(self):
        """Test for a restriction with the "only_contacts" option"""

        sale_order_partner_restrict = "only_contacts"
        self.main_company.sale_order_partner_restrict = sale_order_partner_restrict

        self.assertEqual(
            self.main_company.sale_order_partner_restrict,
            sale_order_partner_restrict,
            "Must be equal to 'only_contacts'",
        )

        self.assertTrue(
            self._create_sale_order(self.partner_child),
            "Contact type partner" "should be available in 'only_contacts' option",
        )

        # Parent type partner shouldn't be available in 'only_contacts' option
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_parent)

        # Partner from another company
        # shouldn't be available on this company (option 'only_contacts')
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_diff_company)

        # Child and other type partner
        # shouldn't be available in 'only_contacts' option
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_delivery)

    def test_sale_order_partner_restrict_option_only_delivery(self):
        """Test for a restriction with the "only_delivery_addresses" option"""

        sale_order_partner_restrict = "only_delivery_addresses"
        self.main_company.sale_order_partner_restrict = sale_order_partner_restrict

        self.assertEqual(
            self.main_company.sale_order_partner_restrict,
            sale_order_partner_restrict,
            "Must be equal to 'only_contacts'",
        )

        self.assertTrue(
            self._create_sale_order(self.partner_delivery_address),
            "Contact type partner"
            "should be available in 'only_delivery_addresses' option",
        )

        # Contact type partner shouldn't be available in
        # 'only_delivery_addresses' option
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_child)

        # Parent type partner shouldn't be available in 'only_delivery_addresses' option
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_parent)

        # Partner from another company
        # shouldn't be available on this company (option 'only_delivery_addresses')
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_diff_company)

        # Child and other type partner
        # shouldn't be available in 'only_delivery_addresses' option
        with self.assertRaises(ValidationError):
            self._create_sale_order(self.partner_delivery)

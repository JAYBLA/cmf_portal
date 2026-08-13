import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from customers.models import Customer
from users.models import CustomUser

from .models import Quotation


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class QuotationCreateHtmxTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="quotation-test-admin",
            password="test-password",
            role=CustomUser.Roles.ADMIN,
        )
        self.client.force_login(self.user)
        self.customer = Customer.objects.create(customer_name="Test Customer")
        self.url = reverse("quotations:quotation_create")

    def tearDown(self):
        for item in Quotation.objects.prefetch_related("items"):
            for quotation_item in item.items.all():
                if quotation_item.image:
                    quotation_item.image.delete(save=False)

    def test_invalid_submission_returns_form_for_modal_swap(self):
        response = self.client.post(
            self.url,
            {
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Save Quotation")
        self.assertContains(response, "Please select or enter a customer")
        self.assertNotIn("HX-Reswap", response.headers)

    def test_successful_submission_closes_without_swapping_modal(self):
        response = self.client.post(
            self.url,
            {
                "customer_text": str(self.customer.pk),
                "title": "Working quotation",
                "quote_date": "2026-08-12",
                "due_date": "2026-08-19",
                "completion_period_from": "1",
                "completion_period_to": "2",
                "completion_period_unit": "weeks",
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
                "items-0-description": "Custom item",
                "items-0-quantity": "2",
                "items-0-unit_price": "1500",
                "items-0-is_tangible": "True",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Reswap"], "none")
        self.assertIn("recordSaved", response.headers["HX-Trigger"])
        self.assertTrue(Quotation.objects.filter(title="Working quotation").exists())

    def test_submission_saves_item_photo(self):
        image = SimpleUploadedFile(
            "item.gif",
            (
                b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00"
                b"\xff\xff\xff,\x00\x00\x00\x00\x01\x00\x01\x00\x00"
                b"\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )
        response = self.client.post(
            self.url,
            {
                "customer_text": str(self.customer.pk),
                "title": "Quotation with photo",
                "quote_date": "2026-08-12",
                "due_date": "2026-08-19",
                "completion_period_from": "1",
                "completion_period_to": "2",
                "completion_period_unit": "weeks",
                "items-TOTAL_FORMS": "1",
                "items-INITIAL_FORMS": "0",
                "items-MIN_NUM_FORMS": "0",
                "items-MAX_NUM_FORMS": "1000",
                "items-0-description": "Photographed item",
                "items-0-image": image,
                "items-0-quantity": "1",
                "items-0-unit_price": "500",
                "items-0-is_tangible": "True",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        item = Quotation.objects.get(title="Quotation with photo").items.get()
        self.assertTrue(item.image.name.endswith("item.gif"))

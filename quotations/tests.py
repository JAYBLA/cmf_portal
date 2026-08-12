from django.test import TestCase
from django.urls import reverse

from customers.models import Customer

from .models import Quotation


class QuotationCreateHtmxTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(customer_name="Test Customer")
        self.url = reverse("quotations:quotation_create")

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

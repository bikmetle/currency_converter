from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class RatesTestCase(TestCase):
    
    def setUp(self):
        self.url = reverse("rates")

    def test_correct_params(self):
        response = self.client.get(self.url, {"from": "USD", "to": "RUB", "value": "2.3"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.json())
    
    def test_wrong_params_keys(self):
        response = self.client.get(self.url, {"form": "USD", "ot": "RUB", "val": "2.3"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["details"], 
            'Please fill in all required keys: `from`, `to` and `value`'
        )

    def test_wrong_params_currency_value(self):
        response = self.client.get(self.url, {"from": "USAD", "to": "RUB", "value": "2.2"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["details"], 
            '`USAD` or `RUB` is not correct'
        )

    def test_wrong_params_amount_value_not_numeric(self):
        response = self.client.get(self.url, {"from": "USD", "to": "RUB", "value": "one"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["details"], 
            '`one` should be a float'
        )

    def test_wrong_params_amount_negative_value(self):
        response = self.client.get(self.url, {"from": "USD", "to": "RUB", "value": "-3.4"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["details"], 
            '`-3.4` should be a positive float'
        )

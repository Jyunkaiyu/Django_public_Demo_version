from django.test import TestCase,TransactionTestCase

# Create your tests here.
from .models import product


class TestModels(TransactionTestCase):
    def test_search(self):
        # product.objects.create(product_name="XXX")
        rv1 = product.objects.filter(product_name__contains="Crucial MX500 500GB")
        # Passes
        self.assertEqual(rv1.count(), 1)

        rv2 = product.objects.filter(product_name__search="Crucial MX500 500GB")
        # Fails - count i
        self.assertEqual(rv2.count(), 1)
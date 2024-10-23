# Create your tests here.
# freshlyapp/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Product

class ProductTests(TestCase):

    def setUp(self):
        Product.objects.create(name="Product1", price=10.0)

    def test_product_list(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product1")

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


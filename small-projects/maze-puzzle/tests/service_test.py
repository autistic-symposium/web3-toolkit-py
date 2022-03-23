import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../src"))

from service import Service


class ProductDetailClientTestDouble:
    def __init__(self):
        self.contents = {}

    def lookup(self, product_token):
        if product_token in self.contents:
            return self.contents[product_token]
        else:
            return None

class ProductSearchClientTestDouble:
    def __init__(self):
        self.search_to_results = {}

    def search_for_all_in_price_range(self, lower_cents, upper_cents, start_record, num_records):
        return self.search_to_results[(lower_cents, upper_cents, start_record, num_records)]

class ServiceTest(unittest.TestCase):
    def setUp(self):
        self.detail_client = ProductDetailClientTestDouble()
        self.search_client = ProductSearchClientTestDouble()
        self.service = Service(self.detail_client, self.search_client)

    def test_lookup_success(self):
        expected_product = {
            "token": "AAA",
            "description": "Red Bike",
            "price_cents": 45000
        }

        self.detail_client.contents["AAA"] = expected_product

        self.assertEqual(
            self.service.lookup("AAA"),
            {"status": 200,
             "product": expected_product})

    def test_lookup_not_found(self):
        self.assertEqual(
            self.service.lookup("AAA"),
            {"status": 404})

    def test_lookup_bad_input(self):
        self.assertEqual(
            self.service.lookup("this-is-not-a-uuid"),
            {"status": 400})

    def test_search_price_range(self):
        brown_bike = {
            "token": "AAA",
            "description": "Brown Bike",
            "price_cents": 10000
        }

        blue_bike = {
            "token": "BBB",
            "description": "Blue Bike",
            "price_cents": 37500
        }

        red_bike = {
            "token": "CCC",
             "description": "Red Bike",
             "price_cents": 45000
        }

        gray_bike = {
            "token": "DDD",
             "description": "Gray Bike",
             "price_cents": 99900
        }

        self.detail_client.contents["AAA"] = brown_bike
        self.detail_client.contents["BBB"] = blue_bike
        self.detail_client.contents["CCC"] = red_bike
        self.detail_client.contents["DDD"] = gray_bike

        self.search_client.search_to_results[(30000, 50000, 0, 10)] = ["BBB", "CCC"]

        self.assertEqual(
            self.service.search_by_price_range(30000, 50000, 0, 10),
            {"status": 200,
             "products": [blue_bike, red_bike]})

if __name__ == '__main__':
    unittest.main()
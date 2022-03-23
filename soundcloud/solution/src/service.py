import re

TOKEN_REGEX = re.compile("^[0-9A-F-]+$")

class Service:
    def __init__(self, product_detail_client, product_search_client):
        self.product_detail_client = product_detail_client
        self.product_search_client = product_search_client

    def lookup(self, product_token):
        """
        Given a valid product token,
        lookup product detail information from the product detail backend service.

        - Results in Bad Request if the token is invalid
        - Results in Not Found if the product is unknown to the backend service
        """
        if not TOKEN_REGEX.match(product_token):
            return {"status": 400}

        lookup_result = self.product_detail_client.lookup(product_token)
        if lookup_result:
            return {"status": 200, "product": lookup_result}
        else:
            return {"status": 404}

    def search_by_price_range(self, lower_cents, upper_cents, start_record, num_records):
        page_of_product_tokens = \
            self.product_search_client.search_for_all_in_price_range(
                lower_cents,
                upper_cents,
                start_record,
                num_records)

        product_detail_results = []
        for product_token in page_of_product_tokens:
            product_detail_results.append(self.lookup(product_token)["product"])

        return {"status": 200, "products": product_detail_results}

if __name__ == "__main__":
    a = Service()
    print(a.lookup('aaa'))
"""
Interview note:
    This is a client "stub", here for demonstration and documentation
    purposes only.

    In a real production environment, this client would send requests over
    the network to a product search backend service.

The product search backend service is responsible for performing lookups
against a product search index (e.g., elasticsearch) and returning product
tokens that are search result "hits".
"""
class ProductSearchClient:

    def search_for_all_in_price_range(lower_cents, upper_cents, start_record, num_records):
        """
        Given a price range plus pagination information,
        returns a list of product tokens of products
        whose price falls in the range.

        The price range is inclusive - that is,
        a given price "p" matches if:

        upper_cents >= p >= lower_cents

        If no products have prices in the price range,
        returns an empty list.

        Product tokens are ordered by price, from lowest to highest.

        Out of the total list of possible product tokens,
        only the "page" of product tokens starting at the list position
        start_record, and ending at start_record+num_records, are returned.

        If start_record+num_records is greater than the number of actual
        result records, the resulting list size will be (accordingly)
        smaller than num_records.

        Example result:

        ["AAA",
         "BBB"]
        """
        pass

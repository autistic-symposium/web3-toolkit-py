"""
Interview note:
    This is a client "stub", here for demonstration and documentation
    purposes only.

    In a real production environment, this client would send requests over
    the network to a product detail backend service.

The product detail backend service is responsible for retrieving product
detail records from its datastore (e.g., a mysql database), and
returning them to callers.
"""
class ProductDetailClient:

    def lookup(product_token):
        """
        Given a product token, makes a blocking call to the lookup endpoint of
        the product detail backend service,
        and returns a corresponding product detail record, if found.
        If no record is found, returns None.

        Example result:

        {"token": "AAA",
         "description": "Red Bike",
         "price_cents": 45000}
        """
        pass

    def batch_lookup(product_tokens):
        """
        Given a list of product tokens, makes a blocking call to the
        batch lookup endpoint of the product detail backend service,
        and returns a map of product token to product detail record, for all
        that are found.
        Any records that cannot be found are ommitted from the result.

        Example result:

        {"AAA": {
            "token": "AAA",
            "description": "Red Bike",
            "price_cents": 45000},
         "BBB": {
            "token": "BBB",
            "description": "Blue Bike",
            "price_cents": 37500}}
        """
        pass
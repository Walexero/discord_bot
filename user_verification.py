from ast import Str
from woocommerce import API
import os

class VerifyUser():

    def __init__(self,email):
        self.email = email

    def _query_api(self, input_query):
        wcapi = API(
            url="https://learn-league.com/",
            consumer_key= os.getenv("PUB_KEY"),
            consumer_secret= os.getenv("PRIV_KEY"),
            wp_api=True,
            verify_ssl = True,
            version="wc/v3",
            query_string_auth = True,
        )
    
        lookup = wcapi.get(input_query).json()
        return lookup

    def subscription_verifier(self, subscribers: str):
        print("Finding Specific subscriber")
        for verify_subscriber_email in subscribers:
            if verify_subscriber_email["email"] == self.email:
                if verify_subscriber_email["is_paying_customer"]:
                    print("You are a subscriber")
                    return verify_subscriber_email["id"]
                else:
                    return "Please Subscribe and try again"
            else:
                pass

    def order_paid_for(self, subscriber):
        print("Getting your payment")
        order_lookup = self._query_api("orders")

        def _get_order(order_details):
            get_subscriber_order_details = order_details["line_items"]
            for subscriber_order in get_subscriber_order_details:
                return subscriber_order["product_id"]

        def _get_product_id(subscriber):
            if subscriber:
                for subscriber_order in order_lookup:
                    if subscriber == subscriber_order["customer_id"]:
                        print("Yes,found you")
                        get_subscriber_order = _get_order(subscriber_order)
                        print("Got your order")
                        return get_subscriber_order
            else:
                return "Please Subscribe"

        return _get_product_id(subscriber)


    def _get_product(self,product_id):
        # def assign_role_normal_user_monthly():
        #     if 

        products = self._query_api("products")

        for product in products:
            #TODO: How to make the function call the required roles for discord_bot execution
            while product["id"] == product_id and product["id"] == 3714:
                return "assign normal account"
            while product["id"] == product_id and product["id"] == 3715:
                return "assign normal yearly account"
            while product["id"] == product_id and product["id"] == 1481:
                return "assign pro account"
            while product["id"] == product_id and product["id"] == 103:
                return "assign pro yearly account"
            else:
                return "You should subscribe to a qualifying plan to get a role"

    # def controller(self):
    #     subscriber_lookup = self.subscription_verifier(self._query_api("customers"), self.email)
    #     if type(subscriber_lookup) is int:
    #         order = self.order_paid_for(subscriber_lookup)
    #         if type(order) is int:
    #             product = self._get_product(order)
    #         else:
    #             return order
    #     else:
    #         return subscriber_lookup
            #TODO: This should be a message.send(letting the user know the outputted error)

    

    
        
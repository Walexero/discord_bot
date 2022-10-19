from ast import Str
from woocommerce import API
import os
 
STANDARD_PACKAGE_MONTHLY = None
STANDARD_PACKAGE_YEARLY = None
PRO_PACKAGE_MONTHLY = None
PRO_PACKAGE_YEARLY = None

def _get_sub_info():

    wcapi = API(
        url="https://learn-league.com/",
        consumer_key= os.getenv("PUB_KEY"),
        consumer_secret= os.getenv("PRIV_KEY"),
        verify_ssl = True,
        version="wc/v3",
        query_string_auth = True,
    )
    l_s = wcapi.get("customers").json()
    print(l_s)

# _get_sub_info()


def _get_subscription_info():
    print("Starting to query API")
    email = input("Enter your email: ")

    def _query_api(input_query):
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
            
    #TODO: Create a nice fail or timeout for exceptions where the lookup fails:not necessary
    

    def subscription_verifier(subscribers:str,customer_email:str):
        print("Finding Specific subscriber")
        for verify_subscriber_email in subscribers:
            print(verify_subscriber_email["email"])
            if verify_subscriber_email["email"] == customer_email:
                if verify_subscriber_email["is_paying_customer"]:
                    print("You are a subscriber")
                    print(verify_subscriber_email["id"])
                    return verify_subscriber_email["id"]
                else:
                    return "Please Subscribe and try again"
            else:
                pass
            

    def _get_product(product_id):
        # def assign_role_normal_user_monthly():
        #     if 

        products = _query_api("products")
        for product in products:
            try:
                #TODO: Write a function that is run if the checked order value falls with a section of the product id
                while product["id"] == product_id and product["id"] == 3714:
                    return "assign normal account"
                while product["id"] == product_id and product["id"] == 3715:
                    return "assign normal yearly account"
                while product["id"] == product_id and product["id"] == 1481:
                    return "assign pro account"
                while product["id"] == product_id and product["id"] == 103:
                    return "assign pro yearly account"
            except:
                return "You should subscribe to a qualifying plan to get a role"
            
    def _payment_order(subscriber,email):
        print("Getting your payment")

        def _get_order(order_details):
            get_subscriber_order_details = order_details["line_items"]
            for subscriber_order in get_subscriber_order_details:
                print(subscriber_order["product_id"])
                return subscriber_order["product_id"]


        def get_product_id(subscriber):
            if subscriber:
                order_lookup = _query_api("orders")
                for subscriber_order in order_lookup:
                    if subscriber == subscriber_order["customer_id"]:
                        print("Yes,found you")
                        get_subscriber_order = _get_order(subscriber_order)
                        print("Got your order")
                        return get_subscriber_order
            else:
                return "Please Subscribe"

        return get_product_id(subscriber)

    
    subscriber_lookup = subscription_verifier(_query_api("customers"), email)
    if type(subscriber_lookup) is int:
        order = _payment_order(subscriber_lookup,email)
        if type(order) is int:
            payment_plan = _get_product(order)
            print("The payment plan", payment_plan)
        else:
            print(order)

    else:
        print(subscriber_lookup)

    # print(lookup_user)

    print("Finished querying API")
_get_subscription_info()
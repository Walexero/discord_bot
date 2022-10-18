from ast import Str
from woocommerce import API
import os

# client = discord.Client()

# @client.event
# async def on_ready():
    # print(f'Bot is live as {client.user}')
# 
# @client.event
# async def on_message(message):
    # if message.author == client.user:
        # return
    # 
    # # if message.channel.name == "bot_test" and message.content.startswith('hello'):
        # await message.channel.send('Hi')
# 
# intents = discord.Intents.default()
# intents.message_content = True
# client.run(TOKEN)
# 
STANDARD_PACKAGE_MONTHLY = None
STANDARD_PACKAGE_YEARLY = None
PRO_PACKAGE_MONTHLY = None
PRO_PACKAGE_YEARLY = None


normal_subscriber_min = 15
normal_subscriber_max = 20
pro_subscriber_min = 45
pro_subscriber_max = 50

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
    # for items in l_s:
    #     if items["email"] == "tester@web.net":
    #         print(items)


# _get_sub_info()


def _get_subscription_info():
    print("Starting to query API")
    email = input("Enter your email: ")

    def _query_api(input_query):
        wcapi = API(
            url="https://learn-league.com/",
            consumer_key= "ck_a482ff0296b8b4a56b74ac4dc0cffbcd9a3d7ed7",
            consumer_secret= "cs_f2e6b2f73ce68d50dd36bcd10b64d0eea2aa1c3f",
            wp_api=True,
            verify_ssl = True,
            version="wc/v3",
            query_string_auth = True,
        )
    
        lookup = wcapi.get(input_query).json()
        return lookup
    
    #TODO: Create a nice fail or timeout for exceptions where the lookup fails

    def _subscription_verifier(subscribers: Str,customer_email):
        print("Finding Specific subscriber")
        for verify_subscriber_email in subscribers:
            #TODO: enable nice error in case the user isn't a user or subscriber at all
            if verify_subscriber_email["email"] == customer_email:
                if verify_subscriber_email["is_paying_customer"]:
                    print("You are a subscriber")
                    return verify_subscriber_email["id"]
                else:
                    print("Please Subscribe and try again")
                    return 

    def _get_product():
        products = _query_api("products")
        for product in products:
            print(product["name"],product["id"])
            #TODO: Write a function that is run if the checked order value falls with a section of the product id
            if product["id"] == 3714:
                STANDARD_PACKAGE_MONTHLY = product["price"]
            if product["id"] == 3715:
                STANDARD_PACKAGE_YEARLY = product["price"]
            if product["id"] == 1481:
                PRO_PACKAGE_MONTHLY = product["price"]
            if product["id"] == 103:
                PRO_PACKAGE_YEARLY = product["price"]

    def _payment_order(subscriber):
        print("Getting your payment")
        def get_order(order_details):
            get_subscriber_order_details = order_details["line_items"]
            for subscriber_order in get_subscriber_order_details:
                print(subscriber_order["product_id"])

        def get_order_payment(order):
            

        if subscriber:
            order_lookup = _query_api("orders")
            for subscriber_order in order_lookup:
                if subscriber == subscriber_order["customer_id"]:
                    print("Yes,found you")
                    get_subscriber_order = get_order(subscriber_order)

                    # print(get_subscriber_order)
                    # get_subscriber_order = subscriber_order["total"]
                    # print(get_subscriber_order)
                    # if get_subscriber_order.find('.'):
                    #     return float(get_subscriber_order)
                    # else:
                    #     return int(get_subscriber_order)
        else:
            pass    

    def get_role(payment_amount):
        print("Getting your role")
        if payment_amount >= normal_subscriber_min and payment_amount <= normal_subscriber_max:
            print("You're a normal Subscriber")
        if payment_amount >= pro_subscriber_min and payment_amount <= pro_subscriber_max:
            print("You're are a pro subscribe! Sensei")

    
    subscriber_lookup = _subscription_verifier(_query_api("customers"), email)
    payment = _payment_order(subscriber_lookup)
    # prod = _get_product()

    # if payment:
    #     get_role(payment)
    print("Finished querying API")
_get_subscription_info()
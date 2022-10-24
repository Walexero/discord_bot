import os
import json
from email_validator import validate_email, EmailNotValidError
from dotenv import find_dotenv, load_dotenv
from woocommerce import API
import asyncio

load_dotenv(find_dotenv())

class VerifyUser:

    def __init__(self,email,initiator):
        self.email = email
        self.initiator = initiator

    async def _email_validator(self,email,query=False):
      try:
        print("validating email")
        email_validation = validate_email(email, check_deliverability=query)
        return email_validation.email

      except EmailNotValidError:
        return "Please retype your email correctly or enter a valid email"

    def _query_api(self, input_query):
      #MULTIPLE QUERYS VARIABLE
      response_holder = []
      lookup = []

      wcapi = API(
        url="https://learn-league.com/",
        consumer_key= "ck_a482ff0296b8b4a56b74ac4dc0cffbcd9a3d7ed7",
        consumer_secret= "cs_f2e6b2f73ce68d50dd36bcd10b64d0eea2aa1c3f",
        wp_api=True,
        verify_ssl = True,
        version="wc/v3",
        query_string_auth = True,
      )

      def _get_total_pages_from_headers():
        lookup_get_header = wcapi.get(input_query,params={
                         "per_page": 50,
                         "page": 1,
                         "role": "all",
                         "order_by": "id"
                       })
        totalpages = lookup_get_header.headers["X-WP-TotalPages"]
        return int(totalpages)

      def _lookup_per_page(pages):
        for page_no in range(pages):
          lookup_page = wcapi.get(input_query,
          params={
                           "per_page": 50,
                           "page": page_no + 1,
                           "role": "all",
                           "order_by": "id"
                         }).json()
          response_holder.append(lookup_page)
    
      pages = _get_total_pages_from_headers()

      def _query_resolver(pages,input_query):
        if pages > 1:
          _lookup_per_page(pages)
          return
        else:
          lookup_page = wcapi.get(input_query,
            params={
                             "per_page": 50,
                             "page": 1,
                             "role": "all",
                             "order_by": "id"
                           }).json()
          return lookup_page

      resolver = _query_resolver(pages,input_query)


      if resolver:
        return resolver
      else:
        for lookups in response_holder:
          for objects in lookups:
            lookup.append(objects)
        return lookup

    async def subscription_verifier(self,subscribers: str, customer_email: str):
      print("Trying again")
      print("Finding Specific subscriber")

      subscriber = [
        verify_subscriber_email for verify_subscriber_email in subscribers
        if verify_subscriber_email['email'] == customer_email
      ]

      if subscriber:
        for verify_subscriber in subscriber:
          if verify_subscriber["is_paying_customer"]:
            print("You are a subscriber")
            return verify_subscriber["id"]

          return "Please subscribe and try again"
      return "Please Subscribe"

    async def _payment_order(self,subscriber):
      print("Getting your payment")
      order_lookup = self._query_api("orders")

      def _get_order(order_details):
        get_subscriber_order_details = order_details["line_items"]
        for subscriber_order in get_subscriber_order_details:
          print(subscriber_order["product_id"])
          return subscriber_order["product_id"]

      def get_product_id(subscriber):
        for subscriber_order in order_lookup:
          if subscriber == subscriber_order["customer_id"]:
            print("yes,found you")
            get_subscriber_order = _get_order(subscriber_order)
            print("Got your order")
            return get_subscriber_order

      return get_product_id(subscriber)

    async def _assign_role_normal_user(initiator, author):
      await author.add_roles(initiator.guild.get_role(1029461048853549056),reason='Subscription verified')
      return "Normal User Assigned"

    async def _assign_role_pro_user(initiator, author):
      await author.add_roles(initiator.guild.get_role(912634472703356945),reason='Subscription verified')
      return "Pro User Assigned"

    async def _subscriber_subscription(self,product_id, message_author, message):

      print("Getting your susbscribed package")
      products = self._query_api("products")

      subscriber_product = [
        product for product in products if product["id"] == product_id
      ]

      subscriber_product_id = [
        subscriber_product_detail["id"]
        for subscriber_product_detail in subscriber_product
      ]

      if subscriber_product_id[0] == 3714 or subscriber_product_id[0] == 3715:
        print("Assigning you normal subscription")
        return await self._assign_role_normal_user(message, message_author)

      elif subscriber_product_id[0] == 1481 or subscriber_product_id[0] == 103:
        return await self._assign_role_pro_user(message, message_author)

      else:
        return "You should subscribe to a qualifying plan to get a role"

    #LOGIC FOR SETTING VALUES FROM THE BASE FUNCTIONS GOES HERE
    async def validate_email(self):
        validator = await self._email_validator(self.email)
        return validator        

    async def lookup_subscriber(self):
        subscriber_lookup = await self.subscription_verifier(self._query_api("customers"), self.email)
        return subscriber_lookup

    async def lookup_subscriber_order(self):
        subscriber_order = await self._payment_order(self.lookup_subscriber)
        return subscriber_order

    async def lookup_subscriber_sub(self):
        subscriber_sub = await self._subscriber_subscription(self.lookup_subscriber_order,self.initiator.author,self.initiator)


    #LOGIC FOR GETTING VALUES FROM THE SET VALUES GOES HERE
    async def get_validated_email(self):
        return await self.validate_email()

    async def get_subscriber(self):
        return await self.lookup_subscriber()

    async def get_subscriber_order(self):
        return await self.lookup_subscriber_order()

    async def get_susbscriber_sub(self):
        return await self.lookup_subscriber_sub()


    #IMPLEMENTS CHECK FOR EACH FUNCTION RETURNED
    async def response_checker(self,function_check,messenger):
        await messenger.channel.send(function_check)
        await asyncio.sleep(30)
        await messenger.channel.delete()
        return

        
    #CONTROLLER FUNCTION
    async def response(self,messenger):
      if await self.get_validated_email() == self.email:
          await messenger.channel.send("Starting to query API")
          if type(await self.get_subscriber()) == int:
              await messenger.channel.send("Finding specific subscriber")
              if type(await self.get_subscriber_order()) == int:
                  await messenger.channel.send("Getting your order")
                  await messenger.channel.send(self.get_subscriber_sub())
                  await asyncio.sleep(30)
                  await messenger.channel.delete()
                  return
              return await self.response_checker(await self.get_subscriber_order(),messenger)
          return await self.response_checker(await self.get_subscriber(),messenger)
      return await self.response_checker(await self.validate_email(),messenger)
  

    
        
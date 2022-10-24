import os
import discord
import json
import asyncio
from email_validator import validate_email, EmailNotValidError
from dotenv import find_dotenv, load_dotenv
from woocommerce import API
from discord.utils import get

load_dotenv(find_dotenv())

TOKEN = os.getenv("BOT_TOKEN")

email_checker = [
  '.com', '.net', '.ru', '.co', '.bru', '.dme', '.me', '.nik', '.email'
]


class MyClient(discord.Client):

  async def on_ready(self):
    print('Logged on as', self.user)

  async def on_message(self, message):

    async def _email_validator(email, query=False):
      try:
        print("validating email")
        email_validation = validate_email(email, check_deliverability=query)
        return email_validation.email

      except EmailNotValidError:
        return "Please retype your email correctly or enter a valid email"

    def _query_api(input_query):
      print("Starting to query API")
      response_holder = []
      lookup = []


      wcapi = API(
        url="https://learn-league.com/",
        consumer_key=os.getenv("PUB_KEY"),
            consumer_secret=os.getenv("PRIV_KEY"),
        wp_api=True,
        verify_ssl=True,
        version="wc/v3",
        query_string_auth=True,
      )

      def _get_total_pages_from_headers():
        lookup_get_header = wcapi.get(input_query,params={
                         "per_page": 25,
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
                           "per_page": 25,
                           "page": page_no + 1,
                           "role": "all",
                           "order_by": "id"
                         }).json()
          response_holder.append(lookup_page)
      _lookup_per_page(_get_total_pages_from_headers())

      for lookups in response_holder:
          for objects in lookups:
              lookup.append(objects)
      return lookup

    async def subscription_verifier(subscribers: str, customer_email: str):
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

    async def _payment_order(subscriber, email):
      print("Getting your payment")
      order_lookup = _query_api("orders")

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
      await author.add_roles(initiator.guild.get_role(1029461048853549056),
                             reason='Subscription verified')
      return "Normal User Assigned"

    async def _assign_role_pro_user(initiator, author):
      await author.add_roles(initiator.guild.get_role(912634472703356945),
                             reason='Subscription verified')
      return "Pro User Assigned"

    async def _get_subscriber_product(product_id, message_author, message):

      print("Getting your susbscribed package")
      products = _query_api("products")

      subscriber_product = [
        product for product in products if product["id"] == product_id
      ]

      subscriber_product_id = [
        subscriber_product_detail["id"]
        for subscriber_product_detail in subscriber_product
      ]

      if subscriber_product_id[0] == 3714 or subscriber_product_id[0] == 3715:
        print("Assigning you normal subscription")
        return await _assign_role_normal_user(message, message_author)

      elif subscriber_product_id[0] == 1481 or subscriber_product_id[0] == 103:
        print("Assigning you pro subscription")
        return await _assign_role_pro_user(message, message_author)
      else:
        return "You should subscribe to a qualifying plan to get a role"

    if message.author == self.user:
      return

    if message.channel.name == "bot-test" and message.content == '/verify':
      sender = message.author
      sender_tag = str(sender)

      msg_notify = f'{sender.mention}, A private ticket has been created for you'
      await message.channel.send(msg_notify)
      msg = f'Hi {sender.mention},  Please provide your email for verification'

      def check(message):
        for email_suffix in email_checker:
          if message.content.endswith(
              email_suffix) and message.channel == ticket_channel:
            return True
        return False

      overwrites = {
        message.guild.default_role:
        discord.PermissionOverwrite(read_messages=False),
        sender:
        discord.PermissionOverwrite(read_messages=True, send_messages=True),
        self.user:
        discord.PermissionOverwrite(read_messages=True, send_messages=True)
      }

      ticket_channel = await message.guild.create_text_channel(
        f'Verification-{sender}', overwrites=overwrites)
      await ticket_channel.send(msg)

      emailmsg = await client.wait_for('message', check=check)
      if emailmsg:
        initiator = emailmsg
        email = emailmsg.content
        author = emailmsg.author
        validator = await _email_validator(email)

        if validator == email:
          await emailmsg.channel.send("Starting to query API")
          lookup_subscriber = await subscription_verifier(
            _query_api("customers"), validator)
        
          if type(lookup_subscriber) == int:
            await emailmsg.channel.send("Finding specific subscriber")
            subscriber_order = await _payment_order(lookup_subscriber,
                                                    validator)
            await emailmsg.channel.send(subscriber_order)

            if type(subscriber_order) == int:
              await emailmsg.channel.send("Getting your order")
              bought_package = await _get_subscriber_product(
                subscriber_order, author, initiator)
              await emailmsg.channel.send(bought_package)
              await asyncio.sleep(30)
              await emailmsg.channel.delete()
              return

            elif type(subscriber_order) == str:
              await emailmsg.channel.send(subscriber_order)
              await asyncio.sleep(30)
              await emailmsg.channel.delete()
              return

          elif type(lookup_subscriber) == str:
            await emailmsg.channel.send(lookup_subscriber)
            await asyncio.sleep(30)
            await emailmsg.channel.delete()
            return

        elif validator != email:
          await emailmsg.channel.send(validator)
          await asyncio.sleep(30)
          await emailmsg.channel.delete()
          return


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)

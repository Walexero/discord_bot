import os
import discord
import json
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
      wcapi = API(
        url="https://learn-league.com/",
        consumer_key="ck_a482ff0296b8b4a56b74ac4dc0cffbcd9a3d7ed7",
        consumer_secret="cs_f2e6b2f73ce68d50dd36bcd10b64d0eea2aa1c3f",
        wp_api=True,
        verify_ssl=True,
        version="wc/v3",
        query_string_auth=True,
      )

      lookup = wcapi.get(input_query,
                         params={
                           "per_page": 100,
                           "page": 1,
                           "role": "all",
                           "order_by": "id"
                         }).json()
      return lookup

    async def subscription_verifier(subscribers: str, customer_email: str):
      print("Finding Specific subscriber")
      print(subscribers)
      # for sub in subscribers:
      #   print(sub)

      # subscriber = [
      #   verify_subscriber_email for verify_subscriber_email in subscribers
      #   if verify_subscriber_email['email'] == customer_email
      # ]

      return

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

    async def _assign_role_normal_user(initiator,author):
      await author.add_roles(
        initiator.guild.get_role(1029461048853549056), reason='Subscription verified'
        )
      return "Normal User Assigned"
      
    
    async def _assign_role_pro_user(initiator,author):
      await author.add_roles(
        initiator.guild.get_role(912634472703356945), reason='Subscription verified'
        )
      return "Pro User Assigned"

    async def _get_subscriber_product(product_id,message_author,message):

      print("Getting your susbscribed package")
      products = _query_api("products")

      subscriber_product = [
        product for product in products  if product["id"] == product_id
      ]
      
      subscriber_product_id = [
        subscriber_product_detail["id"]
        for subscriber_product_detail in subscriber_product
      ]

      if subscriber_product_id[0] == 3714 or subscriber_product_id[0] == 3715:
        print("Assigning you normal subscription")
        return await _assign_role_normal_user(message,message_author)

      elif subscriber_product_id[0] == 1481 or subscriber_product_id[0] == 103:
        print("Assigning you pro subscription")
        return await _assign_role_pro_user(message,message_author)
      else:
        return "You should subscribe to a qualifying plan to get a role"

        
      
    if message.author == self.user:
      return

    if message.channel.name == "bot-test" and message.content == '/verify':
      sender = message.author
      msg = f'Hi @{sender.split},  Please provide your email for verification'
      
      def check(message):
        for email_suffix in email_checker:
          if message.content.endswith(email_suffix) and message.channel==ticket_channel:
            return True
        return False

      overwrites = {
        message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        sender: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        self.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
      }

      ticket_channel = await message.guild.create_text_channel(f'{sender} verification', overwrites=overwrites)
      await ticket_channel.send(msg)


      emailmsg = await client.wait_for('message', check=check)
      if emailmsg:
        initiator = emailmsg
        email = emailmsg.content
        author = emailmsg.author
        validator = await _email_validator(email)


        if validator == email:
          await emailmsg.channel.send("Starting to query API")
          lookup_subscriber = await subscription_verifier(_query_api("customer"), validator)
          return
          if type(lookup_subscriber) == int:
            await emailmsg.channel.send("Finding your subscription")
            subscriber_order = await _payment_order(lookup_subscriber,validator)
            await emailmsg.channel.send(subscriber_order)

            if type(subscriber_order) == int:
              await emailmsg.channel.send("Getting your order")
              bought_package = await _get_subscriber_product(subscriber_order,author,initiator)
              await emailmsg.channel.send(bought_package)
              return

            elif type(subscriber_order) == str:
              await emailmsg.channel.send(subscriber_order)
              return

          elif type(lookup_subscriber) == str:
            await emailmsg.channel.send(lookup_subscriber)
            return

        elif validator != email:
          await emailmsg.channel.send(validator)
          return 



            #     if type(subscriber_order) == int:
            #       await message.channel.send("Getting your order")
            #       bought_package = await _get_subscriber_product(subscriber_order,author,initiator)
            #       await message.channel.send(bought_package)
            #       return

            #     elif type(subscriber_order) == str:
            #       await message.channel.send(subscriber_order)
            #       return

            #   elif type(lookup_subscriber) == str:
            #     await message.channel.send(lookup_subscriber)
            #     return

            # elif validator != email:
            #   await message.channel.send(validator)
            #   return


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)

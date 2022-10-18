import os
import discord
from dotenv import find_dotenv, load_dotenv
import requests
import json
from email_validator import validate_email, EmailNotValidError
from woocommerce import API

load_dotenv(find_dotenv())

server_name = os.getenv("SERVER_NAME")

TOKEN = os.getenv("BOT_TOKEN")
email_checker = ['.com', '.net', '.ru', '.co']

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    # async def on_member_join(member):
    #     await member.create_dm()
    #     await member.dm_channel.send(
    #         f'Hi {member.name}, welcome to my Discord server!'
    #     )

    async def on_message(self, message):

        def _await_event():
            #don't respond to ourselves
            if message.author == self.user:
                return


        def _email_validator(email,query=False):
            try:
                email_validation = validate_email(
                    email,
                    check_deliverability=query
                )
                return email_validation.email

            except EmailNotValidError as e:
                return e

        def _get_subscription_info(subscriber_email):
            print("Starting to query API")

            def _subscription_verifier(subscribers,subscriber_email):
                print("Finding Specific subscriber")
                for verify_subscriber_email in subscribers:
                    
                    if verify_subscriber_email["email"] == subscriber_email:
                        print(verify_subscriber_email)

            wcapi = API(
                url="https://learn-league.com/",
                consumer_key= os.getenv("PUB_KEY"),
                consumer_secret= os.getenv("PRIV_KEY"),
                wp_api=True,
                verify_ssl = True,
                version="wc/v3",
                query_string_auth = True,
            )

            lookup_subscribers = wcapi.get("customers").json()
            print("Finished querying API")
            return _subscription_verifier(lookup_subscribers, subscriber_email)
        


        if message.channel.name == "bot-test" and message.content.startswith('hello') or message.content.startswith('Hello'):
            await message.channel.send('Hi')

        for email_suffix in email_checker: 
            if message.channel.name == "bot-test" and message.content.find(email_suffix):
                email = message.content
                validator = _email_validator(email)

                #TODO: Make sure that the await message waits for the synchronous tasks to complete
                if validator and validator == email:
                    subscribers = _get_subscription_info(validator)

                    #print(validator)

                elif validator and validator != email:
                    await message.channel.send(validator)


             


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)

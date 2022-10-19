import os
import discord
from dotenv import find_dotenv, load_dotenv
import requests
import json
from email_validator import validate_email, EmailNotValidError
from user_verification import VerifyUser

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


        async def _email_validator(email,query=False):
            try:
                email_validation = validate_email(
                    email,
                    check_deliverability=query
                )
                return email_validation.email

            except EmailNotValidError:
                return "Please retype your email correctly or enter a valid email"
        


        if message.channel.name == "bot-test" and message.content.startswith('hello') or message.content.startswith('Hello'):
            await message.channel.send('Hi')

        for email_suffix in email_checker: 
            if message.channel.name == "bot-test" and message.content.find(email_suffix):
                email = message.content
                validator = await _email_validator(email)

                if validator and validator == email:
                    subscribers = _get_subscription_info(validator)

                elif validator and validator != email:
                    await message.channel.send(validator)
                    return


             


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)

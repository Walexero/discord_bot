from mimetypes import init
import os
import discord
from dotenv import find_dotenv, load_dotenv
from user_verification import VerifyUser

load_dotenv(find_dotenv())

server_name = os.getenv("SERVER_NAME")

TOKEN = os.getenv("BOT_TOKEN")

email_checker = [
  '.com', '.net', '.ru', '.co', '.bru', '.dme', '.me', '.nik', '.email'
]

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        async def _await_event():
            #don't respond to ourselves
            if message.author == self.user:
                return
        await _await_event()

        if message.channel.name == "bot-test" and message.content == '/verify':
            sender = message.author
            sender_tag = str(sender)

            msg_notify = f'{sender.mention}, A private ticket has been created for you'
            await message.channel.send(msg_notify)
            msg = f'Hi {sender.mention},  Please provide your email for verification'

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
                verification_init = VerifyUser(email,initiator)
                verified = await verification_init.response(initiator)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)

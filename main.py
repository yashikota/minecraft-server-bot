import lib
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

@tasks.loop(seconds=5)
async def check_active_user(active_user):
    channel = client.get_channel(CHANNEL_ID)
    if active_user != lib.get_active_user():
        active_user = lib.get_active_user()

        if len(active_user) > len(lib.get_logged_in_user()):
            await channel.send(f"{', '.join(active_user)} がログインしました")
        else:
            await channel.send(f"{', '.join(active_user)} がログアウトしました")
        await channel.send(f"現在プレイしているのは {', '.join(active_user)}")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    active_user = lib.get_active_user()
    check_active_user.start(active_user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("login"):
        await message.channel.send(", ".join(lib.get_logged_in_user()))

    if message.content.startswith("logout"):
        await message.channel.send(", ".join(lib.get_logged_out_user()))

    if message.content.startswith("active"):
        await message.channel.send(", ".join(lib.get_active_user()))

client.run(TOKEN)r


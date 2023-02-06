import asyncio
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
async def check_active_user():
    channel = client.get_channel(int(CHANNEL_ID))
    previous_active_user = lib.get_active_user()
    await asyncio.sleep(5)
    now_active_user = lib.get_active_user()

    if previous_active_user != now_active_user:
        if len(previous_active_user) < len(now_active_user):
            await channel.send(f"{lib.get_logged_in_user()[-1]} がログインしました")
        else:
            await channel.send(f"{lib.get_logged_out_user()[-1]} がログアウトしました")
        if len(now_active_user) == 0:
            await channel.send("サーバーに誰もいません")
        else:
            await channel.send(f"現在プレイしているのは {', '.join(now_active_user)} です")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    check_active_user.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("login"):
        await message.channel.send(", ".join(lib.get_logged_in_user()))

    if message.content.startswith("logout"):
        await message.channel.send(", ".join(lib.get_logged_out_user()))

    if message.content.startswith("active"):
        if len(user := lib.get_active_user()) == 0:
            await message.channel.send("サーバーに誰もいません")
        else:
            await message.channel.send(f"現在プレイしているのは {', '.join(user)} です")

client.run(TOKEN)

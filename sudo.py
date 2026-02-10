import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="", intents=intents)

SUDO_USERS = ["PUT_YOUR_DISCORD_ID"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "$help":
        await message.reply("""```bash
BelugaOS Help
ls
pwd
whoami
sudo rm virus.exe
```""")
        return

    content = message.content.strip()
    is_sudo = content.startswith("sudo ")

    if is_sudo and str(message.author.id) not in SUDO_USERS:
        await message.reply(
            f"{message.author.name} is not in the sudoers file.\nThis incident will be reported."
        )
        return

    if content == "ls":
        await message.reply("home  etc  root  virus.exe")

    elif content == "pwd":
        await message.reply("/")

    elif content == "whoami":
        await message.reply("root" if is_sudo else message.author.name)

    elif content.startswith("sudo rm"):
        await message.reply("virus.exe removed.")

bot.run(TOKEN)

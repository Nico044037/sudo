import os
import asyncio
import random
import discord
from discord.ext import commands

# ================= BASIC CONFIG =================
TOKEN = os.getenv("TOKEN")

# 🧑‍💻 USERS WHO CAN USE NORMAL SUDO
SUDO_USERS = {1258115928525373570}  # PUT YOUR DISCORD ID HERE

# 🔒 USERNAME ALLOWED TO USE ;sudo start
START_ALLOWED_USERNAME = "nico044037"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=";",
    intents=intents,
    help_command=None
)

# ================= READY =================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ================= REQUIRED FOR PREFIX COMMANDS =================
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# ================= TERMINAL COMMANDS =================
@bot.command()
async def ls(ctx):
    await ctx.send("home  etc  root  virus.exe")

@bot.command()
async def pwd(ctx):
    await ctx.send("/")

@bot.command()
async def whoami(ctx):
    await ctx.send(ctx.author.display_name)

# ================= SUDO =================
@bot.command()
async def sudo(ctx, action: str, target: discord.Member = None, *, args: str = None):
    # ---------- PERMISSION CHECK ----------
    if ctx.author.id not in SUDO_USERS and action != "start":
        await ctx.send(
            f"{ctx.author.display_name} is not in the sudoers file.\nThis incident will be reported."
        )
        return

    # ---------- sudo start (SPECIAL) ----------
    if action == "start":
        if ctx.author.name != START_ALLOWED_USERNAME:
            await ctx.send(
                "sudo: only nico044037 may run this command"
            )
            return

        await ctx.send("Starting system services...")
        await asyncio.sleep(2)
        await ctx.send("✔️ System started successfully.")
        return

    # ---------- sudo impersonate ----------
    if action == "impersonate":
        if not target or not args:
            await ctx.send("Usage: `;sudo impersonate @user message`")
            return

        # Get or create webhook
        webhooks = await ctx.channel.webhooks()
        webhook = next((w for w in webhooks if w.name == "BelugaSudo"), None)
        if webhook is None:
            webhook = await ctx.channel.create_webhook(name="BelugaSudo")

        # Fake typing delay
        delay = min(5, max(1, len(args) // 10))
        async with ctx.channel.typing():
            await asyncio.sleep(delay)

        await webhook.send(
            content=args,
            username=target.display_name,
            avatar_url=target.display_avatar.url
        )

        # Delete original command
        await ctx.message.delete()
        return

    # ---------- BELUGA-STYLE COMMANDS ----------
    if action == "kill":
        await ctx.send(f"kill: ({args}) - No such process")
    elif action == "killall":
        await ctx.send("💀 Killed all processes (including Discord)")
    elif action == "ban" and target:
        await ctx.send(f"🔨 Banned {target.display_name} (reason: skill issue)")
    elif action == "shutdown":
        await ctx.send("System is going down NOW!")
    elif action == "reboot":
        await ctx.send("Rebooting system...")
    elif action == "apt":
        await ctx.send("Reading package lists...\nDone.")
    elif action == "chmod":
        await ctx.send("chmod: changing permissions of '/': Operation not permitted")
    elif action == "rm" and args == "-rf /":
        await ctx.send("💀 KERNEL PANIC 💀\nSystem destroyed.\nGoodbye.")
    elif action == "rm" and args == "virus.exe":
        await ctx.send("🗑️ virus.exe removed.")
    elif action == "ls":
        await ctx.send("home  etc  root  virus.exe")
    elif action == "whoami":
        await ctx.send("root")
    else:
        await ctx.send(random.choice([
            "sudo: command not found",
            "sudo: permission denied",
            "sudo: segmentation fault",
            "sudo: something went very wrong"
        ]))

# ================= HELP =================
@bot.command()
async def termhelp(ctx):
    await ctx.send("""```bash
BelugaOS Terminal Help

Basic:
;ls
;pwd
;whoami

Sudo:
;sudo ls
;sudo whoami
;sudo rm virus.exe
;sudo rm -rf /
;sudo kill <pid>
;sudo killall
;sudo ban @user
;sudo shutdown
;sudo reboot
;sudo apt install linux
;sudo chmod 000 /
;sudo impersonate @user message

Special:
;sudo start   (nico044037 only)
```""")

# ================= START =================
if not TOKEN:
    raise RuntimeError("TOKEN environment variable not set")

bot.run(TOKEN)

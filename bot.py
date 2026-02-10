import os
import asyncio
import discord
from discord.ext import commands

# ================= BASIC CONFIG =================
TOKEN = os.getenv("TOKEN")

# 🧑‍💻 USERS WHO CAN SUDO
SUDO_USERS = {123456789012345678}  # PUT YOUR ID HERE

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# PREFIX = ;
bot = commands.Bot(
    command_prefix=";",
    intents=intents,
    help_command=None
)

# ================= READY =================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ================= IMPORTANT FIX =================
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
async def sudo(ctx, action: str, member: discord.Member = None, *, message: str = None):
    if ctx.author.id not in SUDO_USERS:
        await ctx.send(
            f"{ctx.author.display_name} is not in the sudoers file.\nThis incident will be reported."
        )
        return

    # ===== sudo impersonate =====
    if action.lower() == "impersonate":
        if not member or not message:
            await ctx.send("Usage: `;sudo impersonate @user message`")
            return

        # Get or create webhook
        webhooks = await ctx.channel.webhooks()
        webhook = next((w for w in webhooks if w.name == "BelugaSudo"), None)

        if webhook is None:
            webhook = await ctx.channel.create_webhook(name="BelugaSudo")

        # ---------- FAKE TYPING DELAY ----------
        delay = min(5, max(1, len(message) // 10))
        async with ctx.channel.typing():
            await asyncio.sleep(delay)

        # Send impersonated message
        await webhook.send(
            content=message,
            username=member.display_name,
            avatar_url=member.display_avatar.url
        )

        # Delete the sudo command for realism
        await ctx.message.delete()
        return

    # ===== normal sudo commands =====
    if action == "rm" and message == "virus.exe":
        await ctx.send("🗑️ virus.exe removed.")
    elif action == "rm" and message == "-rf /":
        await ctx.send("💀 KERNEL PANIC 💀\nSystem destroyed.\nGoodbye.")
    elif action == "ls":
        await ctx.send("home  etc  root  virus.exe")
    elif action == "whoami":
        await ctx.send("root")
    else:
        await ctx.send("sudo: command not found")

# ================= HELP =================
@bot.command()
async def termhelp(ctx):
    await ctx.send("""```bash
BelugaOS Terminal Help

;ls
;pwd
;whoami

;sudo ls
;sudo rm virus.exe
;sudo rm -rf /

;sudo impersonate @user message
```""")

# ================= START =================
if not TOKEN:
    raise RuntimeError("TOKEN environment variable not set")

bot.run(TOKEN)

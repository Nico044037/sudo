import os
import json
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

# ================= BASIC CONFIG =================
TOKEN = os.getenv("DISCORD_TOKEN")import os
import json
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

# ================= BASIC CONFIG =================
TOKEN = os.getenv("DISCORD_TOKEN")
MAIN_GUILD_ID = int(os.getenv("GUILD_ID", "1452967364470505565"))
DATA_FILE = "data.json"

# 🧑‍💻 USERS WHO CAN SUDO
SUDO_USERS = {123456789012345678}  # PUT YOUR ID HERE

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=["!", "?"],
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
            f"{ctx.author.name} is not in the sudoers file.\nThis incident will be reported."
        )
        return

    # ===== sudo impersonate =====
    if action.lower() == "impersonate":
        if not member or not message:
            await ctx.send("Usage: `?sudo impersonate @user message`")
            return

        # Get or create webhook
        webhooks = await ctx.channel.webhooks()
        webhook = next((w for w in webhooks if w.name == "BelugaSudo"), None)

        if webhook is None:
            webhook = await ctx.channel.create_webhook(name="BelugaSudo")

        avatar_url = member.display_avatar.url

        await webhook.send(
            content=message,
            username=member.display_name,
            avatar_url=avatar_url
        )

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

?ls
?pwd
?whoami

?sudo ls
?sudo rm virus.exe
?sudo rm -rf /

?sudo impersonate @user message
```""")

# ================= START =================
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")

bot.run(TOKEN)

MAIN_GUILD_ID = int(os.getenv("GUILD_ID", "1452967364470505565"))
DATA_FILE = "data.json"

# 🧑‍💻 USERS WHO CAN SUDO (PUT YOUR DISCORD ID HERE)
SUDO_USERS = {123456789012345678}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=["!", "?"],
    intents=intents,
    help_command=None
)

# ================= STORAGE =================
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "welcome_channel": None,
                "autoroles": []
            },
            f
        )

with open(DATA_FILE, "r") as f:
    data = json.load(f)

welcome_channel_id = data.get("welcome_channel")
autoroles = set(data.get("autoroles", []))

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "welcome_channel": welcome_channel_id,
                "autoroles": list(autoroles)
            },
            f,
            indent=4
        )

# ================= EMBEDS =================
def rules_embed():
    embed = discord.Embed(
        title="📜 Welcome to the Server!",
        description="Please read the rules carefully ❤️",
        color=discord.Color.red()
    )
    embed.add_field(
        name="💬 Discord Rules",
        value=(
            "🤝 Be respectful\n"
            "🚫 No spamming\n"
            "🔞 No NSFW\n"
            "📢 No advertising\n"
            "⚠️ No illegal content\n"
            "👮 Staff decisions are final"
        ),
        inline=False
    )
    embed.set_footer(text="⚠️ Breaking rules may result in punishment")
    return embed

# ================= READY =================
@bot.event
async def on_ready():
    guild = discord.Object(id=MAIN_GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"✅ Logged in as {bot.user}")

# ================= MEMBER JOIN =================
@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id != MAIN_GUILD_ID:
        return

    await asyncio.sleep(2)

    try:
        await member.send(embed=rules_embed())
    except:
        pass

    for role_id in autoroles:
        role = member.guild.get_role(role_id)
        if role:
            try:
                await member.add_roles(role)
            except:
                pass

    if welcome_channel_id:
        channel = member.guild.get_channel(welcome_channel_id)
        if channel:
            await channel.send(f"👋 Welcome {member.mention}!")

# ================= ⚠️ IMPORTANT FIX =================
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # VERY IMPORTANT: allow prefix commands to work
    await bot.process_commands(message)

# ================= SETUP =================
@bot.tree.command(name="setup", description="Set welcome channel")
@app_commands.checks.has_permissions(manage_guild=True)
async def slash_setup(interaction: discord.Interaction, channel: discord.TextChannel):
    global welcome_channel_id
    welcome_channel_id = channel.id
    save_data()
    await interaction.response.send_message(
        f"✅ Welcome channel set to {channel.mention}", ephemeral=True
    )

@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup(ctx, channel: discord.TextChannel):
    global welcome_channel_id
    welcome_channel_id = channel.id
    save_data()
    await ctx.send(f"✅ Welcome channel set to {channel.mention}")

# ================= TERMINAL HELP =================
@bot.command()
async def termhelp(ctx):
    await ctx.send("""```bash
BelugaOS Terminal Help

ls
pwd
whoami

sudo ls
sudo rm virus.exe
sudo rm -rf /

Prefix required: ? or !
```""")

# ================= TERMINAL COMMANDS =================
@bot.command()
async def ls(ctx):
    await ctx.send("home  etc  root  virus.exe")

@bot.command()
async def pwd(ctx):
    await ctx.send("/")

@bot.command()
async def whoami(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def sudo(ctx, *, command: str):
    if ctx.author.id not in SUDO_USERS:
        await ctx.send(
            f"{ctx.author.name} is not in the sudoers file.\nThis incident will be reported."
        )
        return

    if command == "ls":
        await ctx.send("home  etc  root  virus.exe")
    elif command == "rm virus.exe":
        await ctx.send("🗑️ virus.exe removed.")
    elif command == "rm -rf /":
        await ctx.send("💀 KERNEL PANIC 💀\nSystem destroyed.\nGoodbye.")
    elif command == "whoami":
        await ctx.send("root")
    else:
        await ctx.send(f"sudo: {command}: command not found")

# ================= START =================
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")

bot.run(TOKEN)

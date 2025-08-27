import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up Discord bot with intents and prefix
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="%", intents=intents)

# Custom help command
class MyHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Displays this help message.'
        })

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="📘 Help Menu", color=discord.Color.blue())

        # General
        general = (
            "🛰️ `%ping` — Check if the bot is online\n"
            "❓ `%help` — Show this help message"
        )
        embed.add_field(name="🧭 General", value=general, inline=False)

        # Random & Fun
        fun = (
            "🎰 `%slots` — Play a slot machine game\n"
            "🧠 `%fact` — Get a random fact (`%fact <num, cat>`)\n"
            "😂 `%joke` — Get a random joke\n"
            "💬 `%quote` — Get an inspirational quote\n"
            "🤔 `%if` — Get a random theory\n"
            "🎱 `%8ball <question>` — Ask the magic 8-ball\n"
            "🎲 `%choose <option_1> | <option_2> | ...` — Randomly pick one\n"
            "💣 `%bomb <time> [@user]` — Start a ticking bomb countdown"
        )
        embed.add_field(name="🎲 Random & Fun", value=fun, inline=False)

        # Utilities
        utils = (
            "🌦️ `%weather <city>` — Show weather for a specific city\n"
            "⏰ `%remindme <h> <m> <s> <task>` — Set a reminder\n"
            "🍅 `%pomodoro <work_time_minutes> <break_time_minutes>` — Start a Pomodoro timer\n"
            "📝 `%todo` — Manage your personal to-do list (`%todo help` for details)\n"
            "📊 `%poll <question> | <option_1> | <option_2> | ...` — Create a poll. Use `%poll help` for more details.\n"
            "💵 `%convert <amount> <from> <to>` — Convert currencies"
        )
        embed.add_field(name="🛠️ Utilities", value=utils, inline=False)

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"📗 **Help:** ``%{command.name}``", color=discord.Color.green())

        # Get custom fields from the command
        desc = getattr(command.callback, 'help_description', command.help or "No description available.")
        usage = getattr(command.callback, 'help_usage', f"%{command.name} {command.signature}")
        example = getattr(command.callback, 'help_example', "No example available.")

        embed.add_field(name="**Description**", value=desc, inline=False)
        embed.add_field(name="**Usage**", value=f"``{usage}``", inline=False)
        embed.add_field(name="**Example**", value=f"``{example}``", inline=False)

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        """Custom help for command groups (like %todo)."""
        # Check if the group has custom help attributes
        custom_title = getattr(group.callback, 'help_title', None)
        custom_description = getattr(group.callback, 'help_description', None)
        custom_commands = getattr(group.callback, 'help_commands', None)
        custom_examples = getattr(group.callback, 'help_examples', None)

        if custom_title and custom_description and custom_commands:
            # Use custom embedded help format
            embed = discord.Embed(
                title=custom_title,
                description=custom_description,
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Available Commands", value=custom_commands, inline=False)
            
            if custom_examples:
                embed.add_field(name="Examples", value=custom_examples, inline=False)
            
            embed.set_footer(text=f"Use %help {group.name} <command> for detailed help on a specific command")
            
            await self.get_destination().send(embed=embed)
        else:
            # Fall back to default behavior
            await super().send_group_help(group)

# Assign the custom help command
bot.help_command = MyHelpCommand()

# Ping command
@bot.command()
async def ping(ctx):
    """Check if the bot is online and view its latency."""
    await ctx.send(f"🏓 **Pong!** Latency: {round(bot.latency * 1000)}ms")

# Set help attributes for ping command
ping.callback.help_description = "Check if the bot is online and view its latency."
ping.callback.help_usage = "%ping"
ping.callback.help_example = "%ping"

# On ready event
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Load cogs/extensions
async def main():
    extensions = [
        "cogs.slots",
        "cogs.choose",
        "cogs.poll",
        "cogs.weather",
        "cogs.remindme",
        "cogs.timer",
        "cogs.quotes",
        "cogs.convert",
        "cogs.eightball",
        "cogs.todo",
        "cogs.bomb",
        "cogs.theory"
    ]

    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

    await bot.start(TOKEN)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
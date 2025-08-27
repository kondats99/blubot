import discord
from discord.ext import commands
import random
import os

class Theory(commands.Cog):
    """Cog for responding with random theories from a file."""

    def __init__(self, bot):
        self.bot = bot
        self.theories = self.load_theories()

    def load_theories(self):
        """Load theories from a text file."""
        file_path = os.path.join(os.path.dirname(__file__), "theories.txt")
        if not os.path.exists(file_path):
            print(f"[❌] theories.txt not found at: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines

    @commands.command(name="if")
    async def if_command(self, ctx):
        """
        Respond with a random theory from the list.
        Usage: %if
        """
        if not self.theories:
            await ctx.send("⚠️ No theories found.")
            return

        theory = random.choice(self.theories)
        await ctx.send(f"🤔 **If...** {theory}")

async def setup(bot):
    cog = Theory(bot)
    await bot.add_cog(cog)

    # Help attributes
    cmd = cog.if_command
    cmd.callback.help_description = "Get a random theory."
    cmd.callback.help_usage = "%if"
    cmd.callback.help_example = "%if"

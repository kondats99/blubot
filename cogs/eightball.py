import discord
from discord.ext import commands
import random

class EightBall(commands.Cog):
    """Cog for magic 8-ball functionality."""
    
    def __init__(self, bot):
        self.bot = bot
        self.responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes – definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.", "Don't count on it.",
            "My reply is no.", "My sources say no.",
            "Outlook not so good.", "Very doubtful."
        ]

    @commands.command(name="8ball")
    async def eight_ball(self, ctx, *, question: str):
        """Ask the magic 8-ball a question."""
        answer = random.choice(self.responses)
        await ctx.send(f"🎱 **{answer}**")

async def setup(bot):
    cog = EightBall(bot)
    await bot.add_cog(cog)
    
    # Set help attributes
    cmd = cog.eight_ball
    cmd.callback.help_description = "Ask the magic 8-ball a question."
    cmd.callback.help_usage = "%8ball <question>"
    cmd.callback.help_example = "%8ball Will I pass the exam?"
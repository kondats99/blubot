from discord.ext import commands
import random

class Choose(commands.Cog):
    """Cog for random choice commands."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx, *, options):
        """Let the bot choose one of your options separated by '|'."""
        choices = [opt.strip() for opt in options.split("|") if opt.strip()]
        
        if len(choices) < 2:
            await ctx.send("⚠️ Please provide at least two options separated by '|'")
            return
            
        selection = random.choice(choices)
        await ctx.send(f"🎲 I choose: **{selection}**")

async def setup(bot):
    cog = Choose(bot)
    await bot.add_cog(cog)
    
    # Set help attributes
    cmd = cog.choose
    cmd.callback.help_description = "Let the bot choose one of your options separated by '|'."
    cmd.callback.help_usage = "%choose <option_1> | <option_2> | <option_3> | ..."
    cmd.callback.help_example = "%choose pizza | burger | sushi"
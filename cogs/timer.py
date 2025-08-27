from discord.ext import commands
import asyncio

class StudyTimer(commands.Cog):
    """Cog for Pomodoro study timer."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pomodoro(self, ctx, work: int = 25, rest: int = 5):
        """Start a Pomodoro timer with work and break intervals."""
        
        # Validate input
        if work <= 0 or rest <= 0:
            await ctx.send("⚠️ Work and rest times must be positive numbers.")
            return
            
        # Maximum time limits (in minutes)
        max_work = 120  # 2 hours
        max_rest = 60   # 1 hour
        
        if work > max_work:
            await ctx.send(f"⚠️ Maximum work time is {max_work} minutes.")
            return
            
        if rest > max_rest:
            await ctx.send(f"⚠️ Maximum rest time is {max_rest} minutes.")
            return

        # Start the timer
        await ctx.send(f"🍅 Pomodoro started: {work} minutes of focus!")
        await asyncio.sleep(work * 60)
        
        await ctx.send(f"☕ Break time for {rest} minutes!")
        await asyncio.sleep(rest * 60)
        
        await ctx.send("🔔 Back to work!")

async def setup(bot):
    cog = StudyTimer(bot)
    await bot.add_cog(cog)
    
    # Set help attributes
    cmd = cog.pomodoro
    cmd.callback.help_description = "Start a Pomodoro timer with work and break intervals."
    cmd.callback.help_usage = "%pomodoro <work_time_minutes> <break_time_minutes>"
    cmd.callback.help_example = "%pomodoro 25 5"
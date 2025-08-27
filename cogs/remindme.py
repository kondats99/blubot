from discord.ext import commands
import asyncio
import re

class Reminders(commands.Cog):
    """Cog for reminder functionality."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remindme(self, ctx, *, args):
        """Set a reminder with specified time and message."""
        # Find all time parts (e.g. "1h", "30m", "5s") at the beginning
        time_parts = re.findall(r'(\d+[hms])', args.lower())

        if not time_parts:
            await ctx.send("⚠️ Please specify time using s (seconds), m (minutes), or h (hours).")
            return

        # Create time string as user provided it, maintaining order
        time_str = " ".join(time_parts)

        # Remove time parts from args to get the task
        task = args
        for part in time_parts:
            task = task.replace(part, '', 1)  # Remove only first occurrence

        task = task.strip()
        if not task:
            await ctx.send("⚠️ Please specify a task to remind you about.")
            return

        # Convert time to seconds
        seconds = 0
        for part in time_parts:
            value = int(part[:-1])
            unit = part[-1]
            if unit == 'h':
                seconds += value * 3600
            elif unit == 'm':
                seconds += value * 60
            elif unit == 's':
                seconds += value

        if seconds == 0:
            await ctx.send("⚠️ Time duration must be greater than zero.")
            return

        # Maximum reminder time (24 hours)
        max_seconds = 24 * 3600
        if seconds > max_seconds:
            await ctx.send("⚠️ Maximum reminder time is 24 hours.")
            return

        await ctx.send(
            f"⏰ Okay {ctx.author.mention}, I will remind you in **{time_str}** about **{task}**."
        )
        
        await asyncio.sleep(seconds)
        await ctx.send(f"🔔 {ctx.author.mention} Reminder: **{task}**")

async def setup(bot):
    cog = Reminders(bot)
    await bot.add_cog(cog)
    
    # Set help attributes
    cmd = cog.remindme
    cmd.callback.help_description = "Set a reminder with specified time and message."
    cmd.callback.help_usage = "%remindme <h> <m> <s> <task>"
    cmd.callback.help_example = "%remindme 5m 30s take food out of the oven"
import discord
from discord.ext import commands
import asyncio
import re
from datetime import datetime, timedelta
import random

class Bomb(commands.Cog):
    """Cog for countdown bomb timer."""

    def __init__(self, bot):
        self.bot = bot
        self.active_timers = {}  # key: ctx.message.id, value: dict with end_time, users, time_str

    @commands.group(name="bomb", invoke_without_command=True)
    async def bomb(self, ctx, *, args=None):
        """
        Start a countdown that ends with a big boom!
        Usage: %bomb <time> [@user1] [@user2] ... OR %bomb status
        Example: %bomb 1m 30s @Konstantina @George @Maria
        """
        if args is None:
            await ctx.send("⚠️ Please specify a time or use `%bomb status` to see active timers.")
            return

        if args.lower().strip() == "status":
            await ctx.invoke(self.bomb_status)
            return

        # Extract time parts (e.g. "1h", "30m", "5s")
        time_parts = re.findall(r'(\d+[hms])', args.lower())
        if not time_parts:
            await ctx.send("⚠️ Please specify time using s (seconds), m (minutes), or h (hours).")
            return

        time_str = " ".join(time_parts)

        # Get all mentioned users, or default to command sender
        if ctx.message.mentions:
            mention_targets = [user.mention for user in ctx.message.mentions]
        else:
            mention_targets = [ctx.author.mention]

        # Convert time to total seconds
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

        if seconds <= 0:
            await ctx.send("⚠️ Time must be greater than 0.")
            return

        if seconds > 86400:
            await ctx.send("⚠️ Maximum allowed time is 24 hours.")
            return

        # Format the target list for display
        if len(mention_targets) == 1:
            target_display = mention_targets[0]
        elif len(mention_targets) == 2:
            target_display = f"{mention_targets[0]} and {mention_targets[1]}"
        else:
            target_display = f"{', '.join(mention_targets[:-1])}, and {mention_targets[-1]}"

        await ctx.send(f"🧨 Countdown started for **{time_str}**! Target{'s' if len(mention_targets) > 1 else ''}: {target_display}")

        # Record active timer with end time
        end_time = datetime.utcnow() + timedelta(seconds=seconds)
        self.active_timers[ctx.message.id] = {
            "end_time": end_time,
            "users": mention_targets,
            "time_str": time_str
        }

        # Determine countdown start point
        countdown_start = min(seconds, 10)
        
        # Wait until countdown phase if needed
        if seconds > countdown_start:
            await asyncio.sleep(seconds - countdown_start)

        # Countdown phase
        mentions_str = " ".join(mention_targets)
        for i in range(countdown_start, 0, -1):
            await ctx.send(f"{mentions_str} {i}")
            await asyncio.sleep(1)

        # Generate random explosion message
        explosion_emojis = ["💣", "💥", "💥", "‼️", "🔥", "☠️", "⚠️"]
        min_len = 10
        max_len = 15
        explosion_list = explosion_emojis.copy()
        total_length = random.randint(min_len, max_len)
        while len(explosion_list) < total_length:
            explosion_list.append(random.choice(explosion_emojis))
        random.shuffle(explosion_list)
        explosion_str = "".join(explosion_list)

        await ctx.send(f"{mentions_str} {explosion_str}")

        # Remove timer from active timers after finishing
        self.active_timers.pop(ctx.message.id, None)

    @bomb.command(name="status")
    async def bomb_status(self, ctx):
        """Show all active bomb timers with remaining time and users."""
        if not self.active_timers:
            await ctx.send("✅ There are no active timers right now.")
            return

        embed = discord.Embed(title="⏳ Active Bomb Timers", color=discord.Color.red())
        now = datetime.utcnow()

        for info in self.active_timers.values():
            remaining = info["end_time"] - now
            remaining_seconds = int(remaining.total_seconds())
            if remaining_seconds < 0:
                remaining_seconds = 0
            mins, secs = divmod(remaining_seconds, 60)
            time_fmt = f"{mins}m {secs}s" if mins else f"{secs}s"
            
            # Format users display
            users_list = info["users"]
            if len(users_list) == 1:
                users_display = users_list[0]
            elif len(users_list) == 2:
                users_display = f"{users_list[0]} and {users_list[1]}"
            else:
                users_display = f"{', '.join(users_list[:-1])}, and {users_list[-1]}"
            
            embed.add_field(name=f"User{'s' if len(users_list) > 1 else ''}", value=users_display, inline=True)
            embed.add_field(name=f"Remaining Time", value=f"{time_fmt}", inline=True)
        

        await ctx.send(embed=embed)

async def setup(bot):
    cog = Bomb(bot)
    await bot.add_cog(cog)

    # Help attributes for the group
    bomb_group = cog.bomb
    bomb_group.callback.help_title = "💣 Bomb Commands"
    bomb_group.callback.help_description = "Start countdowns that end with explosive results! Perfect for timing games or creating suspense."
    bomb_group.callback.help_commands = (
        "🧨 `%bomb <time> [@user1] [@user2] ...` — Start a countdown timer\n"
        "⏳ `%bomb status` — Show all active bomb timers"
    )
    bomb_group.callback.help_examples = (
        "`%bomb 1m 30s @Alice @Bob` — 1 minute 30 second countdown for Alice and Bob\n"
        "`%bomb 5s @Alice` — Quick 5 second countdown\n"
        "`%bomb status` — View active timers"
    )

    # Individual command help attributes
    bomb_main = cog.bomb
    bomb_main.callback.help_description = "Start a countdown timer that ends with an explosive message! Supports multiple users and flexible time formats."
    bomb_main.callback.help_usage = "%bomb <time> [@user1] [@user2] ..."
    bomb_main.callback.help_example = "%bomb 1m 30s @Alice @Bob"

    bomb_status_cmd = cog.bomb_status
    bomb_status_cmd.callback.help_description = "Display all currently active bomb timers with remaining time and target users."
    bomb_status_cmd.callback.help_usage = "%bomb status"
    bomb_status_cmd.callback.help_example = "%bomb status"
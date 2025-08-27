from discord.ext import commands
import random
import asyncio

class Slots(commands.Cog):
    """Cog for slot machine game."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slots(self, ctx):
        """Play a 3x3 animated emoji slot machine."""
        emojis = ["🍒", "🍋", "🍀", "💎", "🍇", "🔔"]

        def generate_grid():
            return [[random.choice(emojis) for _ in range(3)] for _ in range(3)]

        # Initial spinning message
        message = await ctx.send("🎰 Spinning...")
        grid = None
        
        # Animate the spinning
        for _ in range(4):
            grid = generate_grid()
            display = "\n".join([" | ".join(row) for row in grid])
            await message.edit(content=f"🎰\n{display}")
            await asyncio.sleep(0.5)

        # Check for wins (horizontal and diagonal)
        win = False
        
        # Check horizontal lines
        for row in grid:
            if len(set(row)) == 1:
                win = True
                break
                
        # Check diagonal lines
        if (grid[0][0] == grid[1][1] == grid[2][2] or 
            grid[0][2] == grid[1][1] == grid[2][0]):
            win = True

        # Send result
        if win:
            await ctx.send("🎉 Congratulations! You hit a combo!")
        else:
            await ctx.send("😢 Better luck next time!")

async def setup(bot):
    cog = Slots(bot)
    await bot.add_cog(cog)
    
    # Set help attributes
    cmd = cog.slots
    cmd.callback.help_description = "Play a 3x3 animated emoji slot machine."
    cmd.callback.help_usage = "%slots"
    cmd.callback.help_example = "%slots"
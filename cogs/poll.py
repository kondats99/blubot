from discord.ext import commands
import discord

class Polls(commands.Cog):
    """Cog for creating polls."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *, args):
        """Create a poll with options, emojis are optional."""
        try:
            parts = [part.strip() for part in args.split("|") if part.strip()]
            
            if len(parts) < 2:
                await ctx.send("⚠️ Usage: `%poll <question> | <emoji_1> <option_1> | <emoji_2> <option_2> | ...`")
                return
                
            question = parts[0]
            options = parts[1:]

            if len(options) < 2:
                await ctx.send("⚠️ You must provide at least two options after the question.")
                return

            default_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            reactions = []
            description_lines = []

            for i, option in enumerate(options):
                option = option.strip()
                
                # Check if option starts with an emoji
                if len(option) >= 3 and option[1] == ' ':
                    emoji, label = option[0], option[2:]
                else:
                    emoji = default_emojis[i] if i < len(default_emojis) else "🔹"
                    label = option

                reactions.append(emoji)
                description_lines.append(f"{emoji} {label}")

            description = question + "\n" + "\n".join(description_lines)
            embed = discord.Embed(
                title="📊 Poll", 
                description=description, 
                color=discord.Color.blurple()
            )

            message = await ctx.send(embed=embed)
            
            # Add reactions
            for emoji in reactions:
                try:
                    await message.add_reaction(emoji)
                except discord.HTTPException:
                    # Skip invalid emojis
                    continue
                    
        except Exception as e:
            await ctx.send(f"⚠️ Error creating poll: {str(e)}")

async def setup(bot):
    cog = Polls(bot)
    await bot.add_cog(cog)
    
    # Set help attributes
    cmd = cog.poll
    cmd.callback.help_description = "Create a poll with 2 or more options, separated by '|'. If no emoji is given, numbers like 1️⃣, 2️⃣, ..., are used by default."
    cmd.callback.help_usage = "%poll <question> | <emoji_1> <option_1> | <emoji_2> <option_2> | ..."
    cmd.callback.help_example = "%poll What's your favorite color? | 🔴 Red | 🟢 Green | 🔵 Blue"
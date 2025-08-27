import discord
from discord.ext import commands
import aiohttp

class FunFacts(commands.Cog):
    """Cog for fun facts, jokes, and quotes."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fact")
    async def fact(self, ctx, category: str = None):
        """Get a random fact or specify category (num, cat)."""
        async with aiohttp.ClientSession() as session:
            try:
                if category is None:
                    url = "https://uselessfacts.jsph.pl/random.json?language=en"
                    emoji = "🧠"
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            fact_text = data.get("text")
                        else:
                            await ctx.send("❌ Could not fetch a fact right now, try again later.")
                            return

                elif category.lower() == "num":
                    url = "http://numbersapi.com/random/trivia?json"
                    emoji = "🧮"
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            fact_text = data.get("text")
                        else:
                            await ctx.send("❌ Could not fetch a number fact right now, try again later.")
                            return

                elif category.lower() == "cat":
                    url = "https://catfact.ninja/fact"
                    emoji = "😺"
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            fact_text = data.get("fact")
                        else:
                            await ctx.send("❌ Could not fetch a cat fact right now, try again later.")
                            return

                else:
                    await ctx.send("❓ Invalid category! Use `%fact`, `%fact num`, or `%fact cat`.")
                    return

                await ctx.send(f"{emoji} **Did you know?** {fact_text}")
                
            except Exception as e:
                await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.command(name="joke")
    async def joke(self, ctx):
        """Get a random joke."""
        emoji = "😂"
        url = "https://official-joke-api.appspot.com/jokes/random"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        setup = data.get("setup")
                        punchline = data.get("punchline")
                        joke_text = f"{setup} ... {punchline}"
                    else:
                        await ctx.send("❌ Could not fetch a joke right now, try again later.")
                        return
                        
            await ctx.send(f"{emoji} {joke_text}")
            
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.command(name="quote")
    async def quote(self, ctx):
        """Get a random inspirational quote."""
        emoji = "💬"
        url = "https://zenquotes.io/api/random"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        quote = data[0].get("q")
                        author = data[0].get("a")
                        quote_text = f'"{quote}" — {author}'
                    else:
                        await ctx.send("❌ Could not fetch a quote right now, try again later.")
                        return
                        
            await ctx.send(f"{emoji} {quote_text}")
            
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

async def setup(bot):
    cog = FunFacts(bot)
    await bot.add_cog(cog)
    
    # Set help attributes for all commands
    fact_cmd = cog.fact
    fact_cmd.callback.help_description = "Get a random fact or specify category (num, cat)."
    fact_cmd.callback.help_usage = "%fact <num, cat>"
    fact_cmd.callback.help_example = "%fact cat"
    
    joke_cmd = cog.joke
    joke_cmd.callback.help_description = "Get a random joke."
    joke_cmd.callback.help_usage = "%joke"
    joke_cmd.callback.help_example = "%joke"
    
    quote_cmd = cog.quote
    quote_cmd.callback.help_description = "Get a random inspirational quote."
    quote_cmd.callback.help_usage = "%quote"
    quote_cmd.callback.help_example = "%quote"
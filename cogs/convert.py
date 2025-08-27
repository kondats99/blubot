import discord
from discord.ext import commands
import aiohttp

class Converter(commands.Cog):
    """Cog for currency conversion."""
    
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://open.er-api.com/v6/latest/"

    @commands.command(name="convert")
    async def convert(self, ctx, amount: float, from_currency: str, to_currency: str):
        """Convert currencies using ISO 4217 codes (e.g. USD, EUR)."""
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}{from_currency}") as resp:
                    if resp.status != 200:
                        await ctx.send(f"❌ Could not fetch exchange rates for {from_currency}.")
                        return
                    data = await resp.json()

            if data.get("result") != "success":
                await ctx.send("❌ Error in API response.")
                return

            rates = data.get("rates", {})
            if to_currency not in rates:
                await ctx.send(f"❌ Currency code `{to_currency}` not found.")
                return

            converted_amount = amount * rates[to_currency]
            await ctx.send(f"💵 {amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

async def setup(bot):
    cog = Converter(bot)
    await bot.add_cog(cog)
    
    # Set help attributes
    cmd = cog.convert
    cmd.callback.help_description = "Convert currencies using ISO 4217 codes (e.g. USD, EUR, GBP, JPY, etc.)."
    cmd.callback.help_usage = "%convert <amount> <from_currency> <to_currency>"
    cmd.callback.help_example = "%convert 100 USD EUR"
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

class Weather(commands.Cog):
    """Cog for weather information."""
    
    def __init__(self, bot):
        self.bot = bot

    def get_weather_emoji(self, description):
        """Get appropriate emoji for weather description."""
        desc = description.lower()
        
        if "clear" in desc:
            return "☀️"
        elif "cloud" in desc:
            return "☁️"
        elif "rain" in desc:
            return "🌧️"
        elif "storm" in desc or "thunder" in desc:
            return "⛈️"
        elif "snow" in desc:
            return "❄️"
        elif "fog" in desc or "mist" in desc:
            return "🌫️"
        else:
            return "🌤️"

    @commands.command()
    async def weather(self, ctx, *, city):
        """Get the current weather for a city."""
        if not API_KEY:
            await ctx.send("❌ Weather service is not configured.")
            return
            
        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric&lang=en"
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()

            if data.get("cod") != 200:
                await ctx.send("❌ City not found.")
                return

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
            emoji = self.get_weather_emoji(desc)
            
            weather_info = (
                f"{emoji} Weather in **{city.title()}**: {desc.title()}\n"
                f"🌡️ Temperature: {temp}°C (feels like {feels_like}°C)\n"
                f"💧 Humidity: {humidity}%"
            )
            
            await ctx.send(weather_info)
            
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

async def setup(bot):
    cog = Weather(bot)
    await bot.add_cog(cog)
    
    # Set help attributes
    cmd = cog.weather
    cmd.callback.help_description = "Get the current weather for a city."
    cmd.callback.help_usage = "%weather <city>"
    cmd.callback.help_example = "%weather Athens"
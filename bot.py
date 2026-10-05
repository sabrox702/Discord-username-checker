import os
import aiohttp
import discord
from discord.ext import tasks

# --- CONFIG ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Your Bot Token
USER_TOKEN = os.getenv("USER_TOKEN")        # Your Account Token (for username check)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")      # Discord Webhook URL
USERNAME_TO_CHECK = "xyro"                  # Username you want to snipe

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

async def is_username_available():
    """Checks if username is available via Discord API"""
    url = "https://discord.com/api/v9/users/@me/pomelo-attempt"
    headers = {
        "Authorization": USER_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {"username": USERNAME_TO_CHECK}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.text()
            print(f"[DEBUG] Response: {data}")
            # If 'taken: false', username is free
            return '"taken": false' in data

@tasks.loop(seconds=45)
async def username_checker():
    try:
        print(f"Checking '{USERNAME_TO_CHECK}'...")
        available = await is_username_available()
        
        if available:
            print(f"USERNAME FOUND: {USERNAME_TO_CHECK} is available!")
            if WEBHOOK_URL:
                async with aiohttp.ClientSession() as session:
                    await session.post(WEBHOOK_URL, json={
                        "content": f"@everyone 🔥 **USERNAME AVAILABLE!** `{USERNAME_TO_CHECK}` is now free! Go claim it!"
                    })
            username_checker.stop()
        else:
            print(f"'{USERNAME_TO_CHECK}' is still taken

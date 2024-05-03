import discord

import ezcord

bot = ezcord.Bot(
    intents=discord.Intents.default()
)

@bot.event
async def on_ready():
    print(f"{bot.user} ist online")

if __name__ == "__main__":
    for filename in ezcord.os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

bot.run("boar")

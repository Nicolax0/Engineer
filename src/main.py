import discord
from discord.ext import commands
from discord import app_commands
import sys

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def setup_hook() -> None:
    await bot.tree.sync()

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name="ping", description="Pong!")
@bot.command()
async def ping(inter: discord.Interaction):
    await inter.response.send_message('Pong!')

@bot.tree.command(name="createteam", description="Creates a team")
@app_commands.describe(name="The name of the team")
@bot.command()
async def createteam(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Creating team {name}")



if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('Usage: python3 commands.py <token>')
    secret = args[1]
    bot.run(secret)
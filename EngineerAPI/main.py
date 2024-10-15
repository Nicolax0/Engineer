from discord.ext import commands
from verification import *
from database import *
import discord
import os

TOKEN = os.getenv("DISCORD_KEY")
SERVER = os.getenv("SERVER_ID")
CHANNEL = int(os.getenv("CHANNEL_ID"))

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Necessary for reading message content

# Create an instance of Bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}')

@bot.command(name='ping')
async def ping(ctx):
    if ctx.channel.id == CHANNEL:
        await ctx.send('pong!')

<<<<<<< HEAD
@bot.command(name='verify')
async def verify(ctx, RCSID: str = None):
    if not RCSID:
        await ctx.send("Please execute the command in the format !verify <RCSID>")
        return
    result = send_verification_code(RCSID, ctx.author.id)
    await ctx.send(f"Email sent to {RCSID + "@rpi.edu"}!\nStatus Code: {str(result)}")

@bot.command(name='createRole')
async def ping(ctx, roleName: str):
    checkRole = discord.utils.get(ctx.guild.roles, name=roleName)
    if checkRole:
        await ctx.send(f"This role already exists.")
    else:
        newRole = await ctx.guild.create_role(name=roleName, reason=f'Role created by {ctx.author.name}')
        await ctx.send(f"Role {newRole.name} has been created.")
            
@bot.command(name='deleteRole')
async def ping(ctx, roleName: str):
    checkRole = discord.utils.get(ctx.guild.roles, name=roleName)
    if not checkRole:
        await ctx.send(f"This role doesn't exist.")
    else:
        await checkRole.delete(reason=f'Role deleted by {ctx.author.name}')
        await ctx.send(f"Role {roleName} has been deleted.")

=======
@bot.command(name='init')
async def init(ctx):
    if ctx.channel.id == CHANNEL:
        connection = connect_to_db()
        if connection is not None:
            print("Connection to database successful")
>>>>>>> Database setup

bot.run(TOKEN)
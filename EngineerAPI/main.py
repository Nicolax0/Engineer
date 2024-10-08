import discord
from discord.ext import commands
from verification import *
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

@bot.command(name='verify')
async def verify(ctx, RCSID: str = None):
    if not RCSID:
        await ctx.send("Please execute the command in the format !verify <RCSID>")
        return
    result = send_verification_code(RCSID, ctx.author.id)
    await ctx.send(f"Email sent to {RCSID + "@rpi.edu"}!\nStatus Code: {str(result)}")

bot.run(TOKEN)

@bot.command(name='graduate')
async def ping(ctx, member: discord.Member = None):
    studentRole = discord.utils.get(ctx.guild.roles, name='Student')
    alumniRole = discord.utils.get(ctx.guild.roles, name='Alumni') 
    
    if studentRole is None:
        await ctx.send("Student role not found.")
        return
    if alumniRole is None:
        await ctx.send("Alumni role not found.")
        return
    
    if member:
        if studentRole in member.roles:
            try:
                await member.remove_roles(studentRole, reason='Graduated')
                await member.add_roles(alumniRole, reason='Graduated')
                await ctx.send(f"{member.display_name} has been graduated from Student to Alumni.")
            except discord.Forbidden:
                await ctx.send(f"Bot lacks permission to modify roles for {member.display_name}.")
            except Exception as e:
                await ctx.send(f"Failed to update roles for {member.display_name}: {e}")
        else:
            await ctx.send(f"{member.display_name} does not have the Student role.")
    
    else:
        membersProcessed = 0
        async with ctx.typing():
            for member in ctx.guild_members:
                if studentRole in member.roles:
                    try:
                        await member.remove_roles(studentRole, reason="Graduated")
                        await member.add_roles(alumniRole, reason='Graduated')
                        membersProcessed += 1
                    except discord.Forbidden:
                        await ctx.send(f"Bot lacks permission to modify roles for {member.display_name}.")
                    except Exception as e:
                        await ctx.send(f"Failed to update roles for {member.display_name}: {e}")
        await ctx.send(f"Processed {membersProcessed} members.")

@bot.command(name='createrole')
async def ping(ctx, roleName: str):
    checkRole = discord.utils.get(ctx.guild.roles, name=roleName)
    if checkRole:
        await ctx.send(f"This role already exists.")
    else:
        newRole = await ctx.guild.create_role(name=roleName, reason=f'Role created by {ctx.author.name}')
        await ctx.send(f"Role {newRole.name} has been created.")
            
@bot.command(name='deleterole')
async def ping(ctx, roleName: str):
    checkRole = discord.utils.get(ctx.guild.roles, name=roleName)
    if not checkRole:
        await ctx.send(f"This role doesn't exist.")
    else:
        await checkRole.delete(reason=f'Role deleted by {ctx.author.name}')
        await ctx.send(f"Role {roleName} has been deleted.")

        
bot.run(TOKEN)
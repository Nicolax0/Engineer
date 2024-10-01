import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_KEY")
SERVER = os.getenv("SERVER_ID")
CHANNEL = int(os.getenv("CHANNEL_ID"))

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Necessary for reading message content
intents.members = True

# Create an instance of Bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}')

@bot.command(name='ping')
async def ping(ctx):
    if ctx.channel.id == CHANNEL:
        await ctx.send('pong!')
        
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
                if student_role in member_roles:
                    try:
                        await member.remove_roles(studentRole, reason="Graduated")
                        await member.add_roles(alumniRole, reason='Graduated')
                        membersProcessed += 1
                    except discord.Forbidden:
                        await ctx.send(f"Bot lacks permission to modify roles for {member.display_name}.")
                    except Exception as e:
                        await ctx.send(f"Failed to update roles for {member.display_name}: {e}")
        await ctx.send(f"Processed {membersProcessed} members.")
                        
bot.run(TOKEN)
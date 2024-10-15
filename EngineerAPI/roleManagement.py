@bot.command(name='removeUserRole')
async def ping(ctx, member: discord.Member, roleName: str):
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    
    if role is None:
        await ctx.send(f"{role} not found.")
        return
    elif role not in member.roles:
        await ctx.send(f"{member.display_name} does not have the {role} role.")
    else:
        try:
            await member.remove_roles(role, reason='Removed role')
            await ctx.send(f"{role} has been removed from {member.display_name}.")
        except discord.Forbidden:
            await ctx.send(f"Bot lacks permission to modify roles for {member.display_name}.")
        except Exception as e:
            await ctx.send(f"Failed to update roles for {member.display_name}: {e}")
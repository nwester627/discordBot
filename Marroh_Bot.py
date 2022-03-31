import discord
import youtube_dl
from discord import FFmpegPCMAudio
from discord.ext import commands
import random


TOKEN = 'OTUzNzMxNjI0NzkxNjA1MjU4.YjI1yg.M6F37qKu0LtXpHiFiEem119bIT8'



client = discord.Client()
client = commands.Bot(command_prefix = "?")

players = {}
randNum = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do that. <:arnoldHalt:953815514164101140>")
        await ctx.message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter all required arguments.")
        await ctx.message.delete()    
    else:
        raise error 

@client.event
async def on_message(message):
    if message.author.id == 206095852274581504:
        randNum = (random.randint(1,1000))
        print(randNum)
        if(randNum == 756):
            await message.channel.send('dn')
    await client.process_commands(message)

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit = amount)

@client.command(pass_context = True)
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided"):
    await member.send(f'You have been kicked from {ctx.message.guild.name}, because: {reason}')
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided"):
    await member.send(f'You have been banned from {ctx.message.guild.name}, because: {reason}')
    await member.ban(reason=reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name,user.discriminator) == (member_name,member.disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " has been unbanned!")
            return

    await ctx.send(member+" was not found")

@client.command(pass_context = True)
async def join(ctx,url):
    if (ctx.author.voice):
        server = ctx.message.author.voice.channel
        voice_client = await server.connect()
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
            vc.play(source)
    else:
        await ctx.send("You must be in a voice channel to run this command")

@client.command()
async def pause(ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")

@client.command()
async def resume(ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resume")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel!")

@client.command()
async def play(ctx,url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
            vc.play(source)



client.run(TOKEN)
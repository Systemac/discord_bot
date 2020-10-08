import discord
from discord.ext import commands

TOKEN = 'NTU3OTEzMDM0OTEyMTcwMDA0.XJI7AQ.UEO2FkZ6xN4qafZ3PGnR7JrfjuQ'

description = '''Bot Python'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """Says Hello World"""
    await ctx.send("Hello World")
    print("Envoi de Hello world")


@bot.command(pass_context=True)
async def move(ctx):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.VoiceChannel):
            if channel == ctx.author.voice.channel:
                await ctx.send(ctx.message.author)
                await ctx.send(ctx.author.voice.channel)


@bot.command(pass_context=True)
async def a2(ctx):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.VoiceChannel):
            if channel == ctx.author.voice.channel:
                await ctx.send(ctx.message.author)
                await ctx.send(ctx.author.voice.channel)


@bot.command()
async def prune(ctx, *nombre):
    print(nombre[0].isdigit())
    channel = ctx.message.channel
    if nombre[0].isdigit():
        messages = await ctx.channel.history(limit=int(nombre[0]) + 1).flatten()
        for message in messages:
            await message.delete()
    elif nombre[0] == 'all':
        await channel.purge(limit=None, check=lambda msg: not msg.pinned)
        # messages = await ctx.channel.history().flatten()
        # for message in messages:
        #     await message.delete()
    elif nombre[0] == 'on':
        print(nombre[1])
        messages = await ctx.channel.history().flatten()
        i = 0
        for _ in reversed(messages):
            await _.delete()
            if i == int(nombre[1] - 1):
                break
            i += 1
    elif nombre[0] == 'off':
        messages = await ctx.channel.history().flatten()
        print(len(messages))
        i = 0
        for _ in messages:
            if i == 0 or i > int(nombre[1]):
                await _.delete()
            i += 1
    print('end')


bot.run(TOKEN)

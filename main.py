import discord
from discord import ChannelType
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
            await ctx.send(f"{channel} : voix")
        elif isinstance(channel, discord.TextChannel):
            await ctx.send(f"{channel} : texte")

@bot.command()
async def prune(ctx, nombre: int):
    messages = await ctx.channel.history(limit=nombre + 1).flatten()
    for message in messages:
        await message.delete()


bot.run(TOKEN)

import json
import os

import discord
from discord.ext import commands
from discord.ext.commands import check

from config.config import config

description = '''Bot Python'''
bot = commands.Bot(command_prefix='!', description=description)


def in_voice_channel():  # check to make sure ctx.author.voice.channel exists
    def predicate(ctx):
        return ctx.author.voice and ctx.author.voice.channel
    return check(predicate)


def save_json_team(js):
    with open("./config/json_team.json", "w") as f:
        json.dump(js, f)


def load_json_team():
    if os.path.exists("./config/json_team.json"):
        with open("./config/json_team.json", 'r') as f:
            return json.load(f)
    else:
        return {}


def save_json_solde(js):
    with open("./config/solde.json", "w") as f:
        json.dump(js, f)


def load_json_solde():
    if os.path.exists("./config/solde.json"):
        with open("./config/solde.json", 'r') as f:
            return json.load(f)
    else:
        return {}


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
async def team(ctx, *args):
    json_team = load_json_team()
    json_team[ctx.message.author.name] = []
    for _ in range(len(args)):
        mm = args[_][3:-1]
        user = bot.get_user(int(mm))
        print(user.name)
        json_team[ctx.message.author.name].append({user.name: user.id})
    save_json_team(json_team)
    await ctx.send(f"{json_team[ctx.message.author.name]}.")


@bot.command(pass_context=True)
async def mvteam(ctx, *args):
    chann = ctx.author.voice.channel
    channel = args[0]
    auteur = ctx.message.author.name
    js = load_json_team()
    if auteur not in js:
        await ctx.send("La team n'as pas été créer.")
    else:
        for chan in ctx.guild.channels:
            if not isinstance(chan, discord.TextChannel):
                # print(f"{chan} _ {channel}")
                if chan.name.lower() == channel.lower():
                    # print("OUIIIIIII")
                    channel = chan
                    break
        for members in chann.members:
            for i in js[auteur]:
                for j, k in i.items():
                    l = bot.get_user(int(k))
                    print(f"{l}{members}")
                    if l == members:
                        await members.move_to(channel)


@bot.command(pass_context=True)
async def lvteam(ctx):
    json_team = load_json_team()
    if json_team[ctx.message.author.name] is not None:
        del json_team[ctx.message.author.name]
    save_json_team(json_team)


@bot.command(pass_context=True)
async def move(ctx, *args):
    auteur = ctx.message.author
    messages = await ctx.channel.history(limit=1).flatten()
    for message in messages:
        await message.delete()
    for arg in args:
        print(arg)
    voice_channel = []
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.VoiceChannel):
            print(channel.name)
            voice_channel.append(channel)
    for _ in voice_channel:
        members = _.members
        print(members)
        print(_)
        if auteur in members:
            await ctx.send(f"{auteur} est sur le canal {_}")
    if len(args) > 1:
        print(args[-1])


@in_voice_channel()
@bot.command()
async def move1(ctx, *args):
    chann = ctx.author.voice.channel
    print(ctx.author.voice.channel.members)
    print(chann)
    channel = args[-1]
    messages = await ctx.channel.history(limit=1).flatten()
    for message in messages:
        await message.delete()
    for chan in ctx.guild.channels:
        if not isinstance(chan, discord.TextChannel):
            print(f"{chan} _ {channel}")
            if chan.name.lower() == channel.lower():
                print("OUIIIIIII")
                channel = chan
                break
    for members in chann.members:
        print(members)
        print(type(members))
        await members.move_to(channel)


@bot.command(pass_context=True)
async def a2(ctx):
    chann = ctx.author.voice.channel
    pass


@bot.command()
async def prune(ctx, *nombre):
    channel = ctx.message.channel
    if not nombre:
        messages = await ctx.channel.history(limit=2).flatten()
        for message in messages:
            await message.delete()
    # print(nombre[0].isdigit())
    elif nombre[0].isdigit():
        messages = await ctx.channel.history(limit=int(nombre[0]) + 1).flatten()
        for message in messages:
            await message.delete()
    elif nombre[0] == 'all':
        await channel.purge(limit=None)
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
    print(f'Fin de suppression des messages du channel {channel}')


bot.run(config.get('TOKEN'))

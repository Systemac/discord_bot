import asyncio
import json
import os
import time

import discord
import requests
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


def save_json_membre(js):
    with open("./config/membre.json", "w") as f:
        json.dump(js, f)


def load_json_membre():
    if os.path.exists("./config/membre.json"):
        with open("./config/membre.json", 'r') as f:
            return json.load(f)
    else:
        return {}


async def gets_items():
    i = requests.get("https://finder.deepspacecrew.com/GetSearch")
    if i.status_code != 200:
        await asyncio.sleep(30)
        await gets_items()
    else:
        dico = {j['id']: j['name'] for j in i.json()}
        with open("./config/items.json", 'w') as f:
            json.dump(dico, f)
        return True


def load_items():
    if os.path.exists("./config/items.json"):
        with open("./config/items.json", 'r') as f:
            return json.load(f)
    else:
        return {}


def containr(text, words):
    # print(words)
    # print(text)
    text.replace('-', ' ')
    # text.replace('-', ' ')
    text.replace('\'', ' ')
    # print(text)
    # print(text)
    for oneWord in words:
        # print(oneWord)
        if oneWord not in text.replace('-', ' ').replace('\'', ' '):
            return False
    return True


def get_item(item):
    dico = {}
    i = load_items()
    if len(i) == 0:
        try:
            a = gets_items()
            if a:
                i = load_items()
            else:
                asyncio.sleep(30)
                get_item(item)
        except:
            asyncio.sleep(30)
            get_item(item)
    for j in i:
        # print(i[j].lower())
        if containr(i[j].lower(), item):
            res = requests.get(f"https://finder.deepspacecrew.com/Search/{j}")
            # print(res.reason)
            dico[i[j]] = res.url + f'Shipshops1/{j}' if len(res.url) < 34 else res.url
            # print("trouvé !")
    if not dico:
        dico = {'rien': 'trouvé'}
    print(f"Envoi des infos sur {item}")
    return dico


async def status_task():
    while True:
        try:
            await gets_items()
        except:
            await asyncio.sleep(10)
        await asyncio.sleep(10000)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.loop.create_task(status_task())


@bot.command()
@commands.has_role("bot")
async def solde(ctx, *args):
    for m in ctx.guild.get_all_member:
        print(m)
    if args[0] == "add":
        user = args[1]
        ajout = args[2]
    elif args[0] == "del":
        user = args[1]
        retire = args[2]


@bot.command(pass_context=True)
@commands.has_role("bot")
async def find(ctx, *args):
    args_ = ' '.join(iter(args))
    if len(args_) < 3:
        await ctx.send("Merci d'envoyer un paramètre à la demande !")
    else:
        await ctx.send(f"Lancement de la recherche sur {args_}.....")
        i = get_item(args)
        embedvar = discord.Embed(title=f'Résultat de la recherche sur {args_} :')
        for key in i:
            embedvar.add_field(name=f"{key} :", value=i[key], inline=False)
        await ctx.send(embed=embedvar)
        # await ctx.send(f"{len(i)} résultat{'s' if len(i) > 1 else ''} pour {args_} :")
        # for key in i:
        #     await ctx.send(f"{key} : {i[key]}")



@bot.command()
@commands.has_role("bot")
async def hello(ctx):
    """Says Hello World"""
    await ctx.send("Hello World")
    print("Envoi de Hello world")


@bot.command(pass_context=True)
@commands.has_role("bot")
async def team(ctx, *args):
    if args[0] == "liste":
        js = load_json_team()
        if len(js) < 1:
            await ctx.send("Pas de team créer pour l'instant.")
            time.sleep(3)
            messages = await ctx.channel.history(limit=2).flatten()
            for message in messages:
                await message.delete()
        else:
            j = [i for i in js]
            await ctx.send(j)
    elif args[0] == "detail":
        name_team = args[1]
        js = load_json_team()
        if name_team in js:
            await ctx.send(f"Detail de la team {name_team}: \n {js[name_team]}.")
        else:
            await ctx.send(f"La team {name_team} n'existe pas.")
        time.sleep(5)
        messages = await ctx.channel.history(limit=2).flatten()
        for message in messages:
            await message.delete()
    elif args[0] == "delete":
        js = load_json_team()
        name_team = args[1]
        if name_team in js:
            del js[name_team]
            save_json_team(js)
        await ctx.send(f"La team {name_team} à été supprimées")
        time.sleep(5)
        messages = await ctx.channel.history(limit=2).flatten()
        for message in messages:
            await message.delete()

    else:
        name_team = args[0]
        json_team = load_json_team()
        json_team[name_team] = []
        for _ in range(len(args) - 1, 0, -1):
            mm = args[_][3:-1]
            user = bot.get_user(int(mm))
            print(user.name)
            json_team[name_team].append({user.name: user.id})
        save_json_team(json_team)
        await ctx.send(f"{json_team[name_team]}.")


@bot.command(pass_context=True)
@commands.has_role("bot")
async def mvteam(ctx, *args):
    chann = ctx.author.voice.channel
    name_team = args[0]
    channel = args[1]
    # auteur = ctx.message.author.name
    js = load_json_team()
    if name_team not in js:
        await ctx.send("La team n'as pas été créer.")
    else:
        for chan in ctx.guild.channels:
            if isinstance(chan, discord.VoiceChannel):
                print(f"{chan} _ {channel}")
                if channel.lower() in chan.name.lower():
                    print("OUIIIIIII")
                    channel = chan
                    break
        print(channel)
        for members in chann.members:
            for i in js[name_team]:
                print(i)
                for j, k in i.items():
                    print(k)
                    l = bot.get_user(int(k))
                    print(f"{l}{members}")
                    if l == members:
                        await members.move_to(channel)


@bot.command(pass_context=True)
@commands.has_role("bot")
async def move(ctx, *args):
    auteur = ctx.message.author
    messages = await ctx.channel.history(limit=1).flatten()
    # for message in messages:
    #     await message.delete()
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
@commands.has_role("bot")
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


@bot.command()
@commands.has_role("bot")
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

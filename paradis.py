import discord
from discord.ext import commands
import random
import aiohttp
import json
import re
import requests

description="A bot written by Omninaut IX for the Paragon section of Marauder Clan"
client=discord.Client()
bot=commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------------")

@bot.command(pass_context=True)
async def hello(ctx):
    """Tests bot activity. Type '!hello' to get a response."""
    await bot.say("Hello, {}!".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def ARAM(ctx):
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://api.agora.gg/gamedata/heroes?lc=en&ssl=true') as resp:
            data = await resp.json()
            heroes = []
            for obj in data["data"]:
                heroes.append(obj["name"])
            #await bot.say(str(heroes))
            chan=ctx.message.author.voice_channel
            players=chan.voice_members.copy()
            players=list(i.mention for i in players)
            if len(players)>10:
                await bot.say("Too many players in {}".format(chan))
                return
            if len(players)<10:
                for i in range(len(players)+1, 11):
                    players.append("Player {}".format(i))
                    hero10=random.sample([heroes,10])
                    team1=random.sample(players, 5)
                    team2=[item for item in players if item not in team1]
                    bundle=[]
                    for i in team1:
                        bundle.append([i,hero10[players.index(i)]])
                    for i in team2:
                        bundle.append([i,hero10[players.index(i)]])
                    await bot.say(
                    "TEAM 1:\n"+
                    "{} - {}\n".format(bundle[0][0],bundle[0][1])+
                    "{} - {}\n".format(bundle[1][0],bundle[1][1])+
                    "{} - {}\n".format(bundle[2][0],bundle[2][1])+
                    "{} - {}\n".format(bundle[3][0],bundle[3][1])+
                    "{} - {}\n\n".format(bundle[4][0],bundle[4][1])+
                    "TEAM 2:\n"+
                    "{} - {}\n".format(bundle[5][0],bundle[5][1])+
                    "{} - {}\n".format(bundle[6][0],bundle[6][1])+
                    "{} - {}\n".format(bundle[7][0],bundle[7][1])+
                    "{} - {}\n".format(bundle[8][0],bundle[8][1])+
                    "{} - {}\n".format(bundle[9][0],bundle[9][1]))
        
@bot.command(pass_context=True)
async def elo(ctx,*,name:str):
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://api.agora.gg/players/search/{}?lc=en&ssl=true'.format(name)) as resp:
            data1=await resp.json()
            try: name=data1["data"][0]["name"]
            except:
                await bot.say("{} not found".format(name))
                return
            id1=data1["data"][0]["id"]
            async with client.get("https://api.agora.gg/players/{}?season=2&lc=en&ssl=true".format(id1)) as final_resp:
                data2=await final_resp.json()
                for i in data2["data"]["stats"]:
                    if i["mode"]==4:
                        elo=i["elo"]
                        rank=i["rank"]
                        kda=float((i["kills"]+i["assists"])/i["deaths"])
                        profile='/'.join(('https://agora.gg/profile', str(id1), str(name)))
                await bot.say("```Name: {name}\nELO: {elo:0.0f}\nKDA: {kda:0.2f}\nRank: {rank}```\nProfile: {profile}".format(name=name,elo=elo,kda=kda,rank=rank, profile=profile))

@bot.command(pass_context=True)
async def card(ctx,*,name:str):
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://api.agora.gg/gamedata/cards?lc=en&ssl=true') as resp:
            json_data=await resp.json(encoding='utf-8')
            for card in json_data['data']:
                if name.casefold() == card['name'].casefold():
                    name = card['name']
                    slotType =card['slotType']
                    cost = card['cost']
                    rarity = card['rarity']
                    affinity = card['affinity']
                    effects = "\n\t".join(["{}: {}".format(*sorted(effect.values(), key=str, reverse=True)) for effect in card['effects']])
                    if not card['maxedEffects']:
                        maxedEffects = 'none'
                    else:
                        maxedEffects = "\n\t".join(["{}: {}".format(*sorted(meffect.values(), key=str, reverse=True)) for meffect in card['maxedEffects']])
            try:
                cost
            except:
                await bot.say("Card not found: {}".format(name))
            else: 
                await bot.say("```Name: {name}\nCost: {cost}\nType: {slotType}\nRarity: {rarity}\nAffinity: {affinity}\nEffects:\n {effects}\n\nFull upgrade bonus:\n {maxedEffects}```".format(name=name,cost=cost,slotType=slotType,rarity=rarity,affinity=affinity,effects=effects,maxedEffects=maxedEffects))

@bot.command(pass_context=True)
async def karta(ctx,*,name):
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://api.agora.gg/gamedata/cards?lc=pl&ssl=true') as resp:
            json_data=await resp.json(encoding='utf-8')
            for card in json_data['data']:
                if name.casefold() == card['name'].casefold():
                    name = card['name']
                    slotType = card['slotType']
                    cost = card['cost']
                    rarity = card['rarity']
                    affinity = card['affinity']
                    effects = "\n\t".join(["{}: {}".format(*sorted(effect.values(), key=str, reverse=True)) for effect in card['effects']])
                    if not card['maxedEffects']:
                        maxedEffects = 'brak'
                    else:
                        maxedEffects = "\n\t".join(["{}: {}".format(*sorted(meffect.values(), key=str, reverse=True)) for meffect in card['maxedEffects']])
            try:
                cost
            except:
                await bot.say("Nie znaleziono karty: {}".format(name))
            else:
                await bot.say("```Name: {name}\nCost: {cost}\nType: {slotType}\nRarity: {rarity}\nAffinity: {affinity}\nEffects:\n {effects}\n\nFull upgrade bonus:\n {maxedEffects}```".format(name=name,cost=cost,slotType=slotType,rarity=rarity,affinity=affinity,effects=effects,maxedEffects=maxedEffects))

@bot.command(pass_context=True)
async def hero(ctx,*,name:str):
    await bot.delete_message(ctx.message)
    async with aiohttp.ClientSession() as client:
        async with client.get('https://api.agora.gg/gamedata/heroes?lc=en&ssl=true') as resp1:
            json_data1=await resp1.json(encoding='utf-8')
            for chemp in json_data1['data']:
                if name.casefold() == chemp['name'].casefold():
                    heroID = chemp['id']
                    async with client.get('https://api.agora.gg/gamedata/heroes/{}?lc=pl&ssl=true'.format(heroID)) as resp2:
                        hone=await resp2.json(encoding='utf-8')
                        name = hone['data']['name']
                        attack = hone['data']['attack']
                        affinity1 = hone['data']['affinity1']
                        affinity2 = hone['data']['affinity2']
                        damageType = hone['data']['damageType']
                        abilities = []
                        for skill in hone['data']['abilities']:
                            sname = skill['name']
                            desc = skill['description']
                            abilities.append(': '.join((str(sname), str(desc))))
            try:
                 heroID
            except:
                await bot.say("Hero not found: {}".format(name))
            else:
                await bot.say("```Name: {name}\nAttack: {attack}\nAffinity: {affinity1} {affinity2}\nDamage: {damageType}\n\nAbilities:\n 1. {skill1}\n\n 2. {skill2}\n\n 3. {skill3}\n\n 4. {skill4}\n\n 5. {skill5}```".format(name=name,attack=attack,affinity1=affinity1,affinity2=affinity2,damageType=damageType,skill1=abilities[0],skill2=abilities[1],skill3=abilities[2],skill4=abilities[3],skill5=abilities[4]))

@bot.command(pass_context=True)
async def h(ctx): 
    await bot.delete_message(ctx.message)
    await bot.say("```Bot commands available:\n\n!h - List of commands\n\n!elo  <player name> - Player stats (usage ex: !elo Andrzej)\n\n!card <card name>  - Cards info (ex: !card Quantum Casing)\n\n!karta <card name>  - Cards PL (ex: !karta Skorupa kwantowa)\n\n!hero <hero name>  - Hero overview (usage ex: !hero Gideon)\n\n!ARAM - Generate hero assignment for 5/5 game\n```".format(ctx.message))

if __name__ == "__main__":
    bot.run('token')

# -*- encoding: utf-8 -*-

import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import re
import os
import time 
import os.path
import sqlite3
import asyncio
import json
import requests
import jishaku
from Cybernator import Paginator
import psutil as ps
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["RodinaBD"]
roles = db["role"]

PREFIX = '!'

intents = discord.Intents.default()
intents.members = True

reports = db["reports"]

async def get_prefix(bot, message):
    if message.guild == None:
        return
    guildid = int(message.guild.id) 
    if reports.count_documents({"guild_id": guildid, "proverka": 1}) == 0:
        return "!"
    return reports.find_one({"guild_id": guildid, "proverka": 1})["prefix"]

bot = commands.Bot(command_prefix = get_prefix, intents=intents)
bot.remove_command('help')

def bytes2human(number, typer=None):
    if typer == "system":
        symbols = ('KБ', 'МБ', 'ГБ', 'TБ', 'ПБ', 'ЭБ', 'ЗБ', 'ИБ')
    else:
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y') 

    prefix = {}

    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if number >= prefix[s]:
            value = float(number) / prefix[s]
            return '%.1f%s' % (value, s)

    return f"{number}B"
    
    '''
    for i in reports.find({"proverka": 1}):
        if not i["rchannel"] == 'None':
            try:
                print(i["mteh"])
                channel = bot.get_guild(i["guild_id"]).get_channel(i["rchannel"])
                message = await channel.fetch_message(i["mteh"])
                embed = discord.Embed(title = 'Сервер технической поддержки бота', description = f'Здравствуйте дорогие пользователи `reporter-бота`, как ваше настроение? ❤\n\nС сегодняшнего дня, наша команда открывает сервер технической поддержки нашего бота!\n`Ссылка на сервер:` https://discord.gg/HXA7jmT\n\n❔ `| Зачем он нужен?`\n> Именно там, вы сможете задать любой вопрос по работе бота, оставить своё предложение по улучшению или сообщить о какой-либо ошибке нашим разработчикам.\n\n🔸 `| Информация`\n> Данный дискорд, является игровым дискордом одного из наших спонсоров, именно по этому, для тех.поддержки бота отведён отдельный канал.\n> Для того что бы получить доступ к нему, необходимо получить роль.\n> Сделать это, можно командой: `!irep`\n\nОстальная информация уже указана в закреплённом сообщении в этом канале, который имеет название `『✨』reported-agents`\n**Хорошего дня и прекрасного настроения!**', color = 0xFB9E14)
                embed.set_footer(text = 'Данное сообщение будет автоматически удалено через 2 дня', icon_url = bot.user.avatar_url)
                try:
                    await message.edit(embed = embed)
                except:
                    print('error')
                    pass
            except:
                pass
    '''

@bot.event
async def on_ready():
    bot.load_extension('cogs.report')
    bot.load_extension('cogs.logs')
    bot.load_extension('cogs.otdeli')
    print('Репортный бот запущен.')
bot.load_extension('cogs.debug')


@bot.command()
async def irep(ctx):
    if not ctx.guild.id == 577511138032484360:
        return

    await ctx.message.delete()

    if discord.utils.get(ctx.guild.roles, id = 814505915695890472) in ctx.author.roles:
        return

    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id = 814505915695890472))
    return await ctx.channel.send(embed = discord.Embed(description = f'{ctx.author.mention}, роль пользователя `reporter-бота` успешно выдана.'), delete_after = 10)

@bot.command(aliases=["bot", "botinfo", "ботинфо"],brief="Информация о боте",usage="бот <None>",description="Подробная информация о боте")
async def _bot(ctx):
    memberbot = discord.utils.get(ctx.guild.members, id = 729309765431328799)
    await ctx.message.delete()

    members_count = 0
    guild_count = len(bot.guilds)

    for guild in bot.guilds:
        members_count += len(guild.members)

    embed1 = discord.Embed(title=f"Информация о боте {memberbot}",
                            description="Бот был написан для удобной работы discord-серверов в области технической поддержки.",
                            color=0xFB9E14)
    embed1.add_field(name=f'Бота создали:', value="dollar ム baby#3603", inline=True)
    embed1.add_field(name=f'Помощь в создании:', value="Google, Документация Discord.py", inline=True)
    embed1.add_field(name="‎‎‎‎", value="‎", inline=True)
    embed1.add_field(name=f'Бот написан на:', value="Discord.py", inline=True)
    embed1.add_field(name=f'Префикс:', value = f'`Префикс данного сервера:` {reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}', inline = False)
    embed1.add_field(name=f'Лицензия:', value="CC BY-SA-NC", inline=True)
    embed1.add_field(name="‎‎‎‎", value="‎", inline=True)
    embed1.add_field(name=f'Участников:', value=f"{members_count}", inline=True)
    embed1.add_field(name=f'Серверов:', value=f"{guild_count}", inline=True)
    embed1.add_field(name=f'Шардов:', value=f"{bot.shard_count}", inline=True)
    embed1.add_field(name=f'Приглашение Бота:',
                        value="[Кликабельная ссылка](https://discord.com/api/oauth2/authorize?client_id=729309765431328799&permissions=8&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Flogin&scope=bot)",
                        inline=True)
    embed1.add_field(name=f'Сервер спонсора:', value="[Тык](https://discord.gg/HXA7jmT)",
                        inline=True)
    embed1.set_thumbnail(url = memberbot.avatar_url)
    

    # ==================

    mem = ps.virtual_memory()
    ping = bot.latency

    ping_emoji = "🟩🔳🔳🔳🔳"
    ping_list = [
        {"ping": 0.00000000000000000, "emoji": "🟩🔳🔳🔳🔳"},
        {"ping": 0.10000000000000000, "emoji": "🟧🟩🔳🔳🔳"},
        {"ping": 0.15000000000000000, "emoji": "🟥🟧🟩🔳🔳"},
        {"ping": 0.20000000000000000, "emoji": "🟥🟥🟧🟩🔳"},
        {"ping": 0.25000000000000000, "emoji": "🟥🟥🟥🟧🟩"},
        {"ping": 0.30000000000000000, "emoji": "🟥🟥🟥🟥🟧"},
        {"ping": 0.35000000000000000, "emoji": "🟥🟥🟥🟥🟥"}
    ]
    for ping_one in ping_list:
        if ping <= ping_one["ping"]:
            ping_emoji = ping_one["emoji"]
            break

    embed2 = discord.Embed(title='Статистика Бота', color=0xFB9E14)

    embed2.add_field(name='Использование CPU',
                        value=f'В настоящее время используется: {ps.cpu_percent()}%',
                        inline=True)

    embed2.add_field(name='Использование RAM',
                        value=f'Доступно: {bytes2human(mem.available, "system")}\n'
                            f'Используется: {bytes2human(mem.used, "system")} ({mem.percent}%)\n'
                            f'Всего: {bytes2human(mem.total, "system")}',
                        inline=True)

    embed2.add_field(name='Пинг Бота',
                        value=f'Пинг: {ping * 1000:.0f}ms\n'
                            f'`{ping_emoji}`',
                        inline=True)

    embed2.set_thumbnail(url = memberbot.avatar_url)

    embeds = [embed1, embed2]

    message = await ctx.send(embed=embed1)
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=embeds, language="ru", footer_icon=bot.user.avatar_url, timeout=120, use_exit=True, delete_message=True, color=0xFB9E14, use_remove_reaction=True)
    await page.start()

tokens = ('NzI5MzA5NzY1NDMxMzI4Nzk5.XwHEpQ.eC2EUwcEblO_HaoX5gCinF27XI8')
bot.run(tokens)

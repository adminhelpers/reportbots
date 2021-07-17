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
from Cybernator import Paginator
import jishaku
import wikipedia
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["RodinaBD"]
reports = db["reports"]
moder = db["moders"]
logged = db["logs"]

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: Family) 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _id) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

def add(guild, member: discord.Member, arg):
  if moder.count_documents({"guild": guild, "id": member.id}) == 0:
    moder.insert_one({"guild": guild, "id": member.id, "close": 0, "rasm": 0, "repa": 0, "addme": 0, "addrep": 0})
    moder.update_one({"guild": guild, "id": member.id}, {"$set": {arg: 1}})
  else:
      moder.update_one({"guild": guild, "id": member.id}, {"$set": {arg: moder.find_one({"guild": guild, "id": member.id})[arg] + 1}})

def setembed(text, url):
    embed = discord.Embed(description = f'{text}', colour=0xFB9E14)
    embed.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = url)

    return embed

global register
register = [ ]

class report(commands.Cog):
    """REPORT Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Report by dollar ム baby#3603 - Запущен')

    @commands.Cog.listener()
    async def on_guild_join(self, guild): 
        info = reports.find_one({"proverka": 2})
        channel = await guild.create_text_channel(f'репорт-бот-настройка', overwrites=None, reason='Присоединение к серверу')
        await channel.set_permissions(guild.default_role, read_messages = False)
        mes = await channel.send(embed = setembed(f'Доброго времени суток!\nМеня зовут бот Репортер и я, буду Вашим верным помощником!\n\n> `Мой создатель:` [{info["discord"]}]({info["vk"]})\n> `Сервер технической поддержки:` {info["server"]}\n\nСпасибо за то, что используете меня.\nДля начала работы со мной, нажмите на ▶', url = self.bot.user.avatar_url))
        await mes.add_reaction('▶')
        reports.insert_one({"guild_id": guild.id, "proverka": 1, "rchannel": "None", "category_id_one": 0, "category_id_two": 0, "category_id_three": 0, "number": "None", "vsego": 0, "close": 0, "active": 0, "himes": "None", "donate": 1, "last_name": "None", "channel": 0, "message_id": 0, "footer": "None", "image": "None", "logchan": 0, "prefix": "!", "support_role": 0, "start_channel": channel.id})
        logged.insert_one({"guild_id": guild.id, "voice": 0, "voicechannel": 0, "channels": 0, "channelschannel": 0, "roleedit": 0, "roleeditchannel": 0, "message": 0, "messagechannel": 0, "roleadd": 0, "roleaddchannel": 0, "category": 0})
        reports.insert_one({"guild_id": guild.id, "proverka": 3, "sender": 1, "ocenka": 1})
        # rchannel - Канал куда задают | category_id_one - Канал с репортами | category_id_two - Канал с репортами на рассмотрении | category_id_three - Корзина | number - Число репортов | himes - Писать ли сообщение после отправики ембеда в канал репорта | donate - Доп функции | channel - Канал с первым сообщением | message_id - Первое сообщение | footer - Футер первого сообщения в канале репорта | image - Картинка в первом сообщении | logchan - Канал логов | prefix - ! | support_role - Роль саппортов | start_channel - Канал с сообщением настройки

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if not reports.count_documents({"guild_id": guild.id, "proverka": 1}) == 0:
            reports.delete_one({"guild_id": guild.id, "proverka": 1})
            try:
                reports.delete_one({"guild_id": guild.id, "proverka": 3})
            except:
                pass

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def prefix(self, ctx, prefix: str = None):
        await ctx.message.delete()
        prefix1 = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if prefix is None:
            return await ctx.send(embed = setembed(f'Префикс установленный на данном сервере: **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}**\n`[P.S]: Для изменения префикса используйте` {prefix1}prefix [prefix]', self.bot.user.avatar_url), delete_after = 20)
        reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"prefix": prefix}})
        await ctx.send(embed = setembed(f'Вы успешно изменили префикс для этого сервера.\n\n`Логирование действия:`\n> `Действие:` **Изменение префикса**\n> `Новый префикс:` **{prefix}**\n> `Старый префикс:` **{prefix1}**\n> `Изменил:` {ctx.author.mention}`({ctx.author})`', self.bot.user.avatar_url), delete_after = 30)

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.member)
    async def help(self, ctx):
        await ctx.message.delete()
        info = reports.find_one({"proverka": 2})
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})
        await ctx.send(f'{ctx.author.mention},', embed = discord.Embed(title = 'Основная информация', description = f'**Привет! Меня зовут бот Репортер!\n\n🔺 `| Поверхностная информация:`\n> `Мой создатель:` [{info["discord"]}]({info["vk"]})\n> `Сервер технической поддержки:` {info["server"]}\n> `Префикс установленный на этом сервере:`   {prefix}\n> `Ссылка на добавление бота:` https://discord.com/api/oauth2/authorize?client_id=729309765431328799&permissions=8&scope=bot **\n\n\n🔹 `| Список моих команд:`\n> `1.` **{prefix}settings** - Настройки для бота`(Категории, роль технической поддержки и т.п)`\n> `2.` **{prefix}setimage** - Установка изображения в изначальное сообщение технической поддержки\n> `3.` **{prefix}setfooter** - Установка подписи под сообщениями в репортах\n> `4.` **{prefix}sethimes** - Установка фантомного сообщения в канале с новым репортом\n> `5.` **{prefix}imoder @Пользователь#1234** - Статистика модератора.\n> `6.` **{prefix}leave** - Отключить бота от сервера\n> `7.` **{prefix}reload** - Пройти регистрацию в базе данных заново\n> `8.` **{prefix}prefix** - Изменить/Узнать префикс сервера.\n\n🔸 `| Информация для технической поддержки:`\n> - `Команды используемые в репортах находятся в канале` <#{rep["logchan"]}>\n> - `Репорт-команды необходимо использовать в канале репорта`\n> - `Для использования репорт-команд необходима роль технической поддержки(`<@&{rep["support_role"]}>`)`\n> - `Для создания вопроса, необходимо написать его в канал` <#{rep["rchannel"]}>\n\n💰 **Приобретение дополнительных функций возможно только у разработчика([{info["discord"]}]({info["vk"]}))**', colour = 0xFB9E14), delete_after = 300)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):

        if channel.guild == None:
            return

        if reports.count_documents({"start_channel": channel.id, "proverka": 1}) == 0:
            return 

        rep = reports.find_one({"start_channel": channel.id, "proverka": 1})
        guild = self.bot.get_guild(rep["guild_id"])

        async for entry in guild.audit_logs(action = discord.AuditLogAction.channel_delete):
            if entry.user.id == 729309765431328799:
                return
            try:
                await guild.leave()
                reports.delete_one({"start_channel": channel.id, "proverka": 1})
            except:
                pass
            try:
                register.remove(guild.id)
            except:
                pass


    #команды:
    # setimage - Изменение картинки начального embed'a
    # setfooter - Добавление подписи под Embed сообщений
    # settings: 
    # 1. Изначальный канал
    # 2. Категории (вопросы | рассмотрение | корзина)
    # 3. Роль Support Team
    # 4. Канал логов
    # sethimes - Добавить сообщение после репорта.
    # reload - Регистрация заново

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def settings(self, ctx):
        if ctx.guild == None:
            return

        if not reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 1:
            return

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})
        if rep["start_channel"] > 0:
            return await ctx.send(embed = setembed(f'Для начала работы со мной, необходимо пройти регистрацию в базе данных.\n`Закончите регистрацию в канале` <#{rep["start_channel"]}>\n\n**Если произошла ошибка и необходимо пройти регистрацию заново, введите `!reload`**', self.bot.user.avatar_url), delete_after = 10)

        if ctx.channel.id == rep["rchannel"]:
            return

        await ctx.message.delete()
        
        for sfd in range(0, 100):
            if rep["donate"] == 0:
                mas = ['1⃣', '2⃣', '3⃣', '4⃣', '✖']
                setting = await ctx.send(embed = setembed(f'**Вы попали в меню изменения настроек технической поддержки**\nВам необходимо выбрать пункт, который Вас интересует:\n\n> 1⃣ `Изменить канал написания вопросов(`<#{rep["rchannel"]}>`)`\n> 2⃣ `Изменить категории с вопросами(Корзина | Активные | Находящиеся на рассмотрении)`\n> 3⃣ `Изменить роль технической поддержки сервера(`<@&{rep["support_role"]}>`)`\n> 4⃣ `Изменить канал для логирования репортов(`<#{rep["logchan"]}>`)`\n\n> ✖ **Закрыть меню**.', self.bot.user.avatar_url))
            elif rep["donate"] == 1:
                if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 3}) == 0:
                    reports.insert_one({"guild_id": ctx.guild.id, "proverka": 3, "sender": 1, "ocenka": 1})
                mas = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '✖']
                setting = await ctx.send(embed = setembed(f'**Вы попали в меню изменения настроек технической поддержки**\nВам необходимо выбрать пункт, который Вас интересует:\n\n> 1⃣ `Изменить канал написания вопросов(`<#{rep["rchannel"]}>`)`\n> 2⃣ `Изменить категории с вопросами(Корзина | Активные | Находящиеся на рассмотрении)`\n> 3⃣ `Изменить роль технической поддержки сервера(`<@&{rep["support_role"]}>`)`\n> 4⃣ `Изменить канал для логирования репортов(`<#{rep["logchan"]}>`)`\n> 5⃣ `Настроить систему логирования`\n> 6⃣ `Настроить систему принятия репортов`\n> 7⃣ `Настроить систему оценки модераторов`\n\n> ✖ **Закрыть меню**.', self.bot.user.avatar_url))
            for i in mas:
                await setting.add_reaction(i)
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in mas)
            except Exception:
                return await setting.delete()
            else:
                if str(react.emoji) == '1⃣':
                    adsp = 1
                    try:
                        await setting.clear_reactions()
                    except:
                        pass
                    await setting.edit(embed = setembed(f'**Укажите новый канал для написания вопросов | Разрешено указывать ID**\n`Для автоматического создания введите` **+**\n\n`Отменить действие можно словом` отмена', self.bot.user.avatar_url))
                    def check(m):
                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                    try:
                        msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                    except Exception:
                        return await setting.delete()
                    else:
                        try:
                            chans, message_id = await self.bot.get_channel(rep["channel"]), rep["message_id"]
                        except:
                            pass
                        emb23 = discord.Embed(description = f'Доброго времени суток! Вы попали в канал технической поддержки сервера **{ctx.guild.name}**.\nТут Вы можете узнать, как получить техническую поддержку от наших модераторов <@&{rep["support_role"]}>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
                        emb23.set_author(name=f'{ctx.guild.name} | Support', icon_url='https://mydovidka.com/wp-content/uploads/2019/11/de0e202e9992854eade6f1ddf73dff49.png')
                        emb23.add_field(name = 'Правила создания репорта', value = '```> Запрещены сообщения не несущие информации или вопроса.\n> Запрещено использовать ненормативную лексику.\n> Запрещено флудить @упоминаниями.\n> Запрещено создавать репорт с некорректным вопросом.\n> Запрещено оскорбительное и неадекватное поведение.\n> Для того что бы задать вопрос, вам необходимо написать его в этот канал.```', inline = False)
                        emb23.add_field(name=f'Общее количество', value=f'**⚙** `{rep["vsego"]}` вопросов', inline = True)
                        emb23.add_field(name = 'На рассмотрении', value = f'**⚙** `{rep["active"]}` вопросов', inline = True)
                        emb23.add_field(name = 'Обработано', value = f'**⚙** `{rep["close"]}` вопросов\n', inline=True)
                        emb23.set_thumbnail(url=ctx.guild.icon_url)
                        emb23.add_field(name = 'Последний вопрос от:', value=f'`{rep["last_name"]}`', inline = False)
                        if rep["image"] == "None":
                            emb23.set_image(url= 'https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif')
                        else:
                            emb23.set_image(url= rep["image"])
                        emb23.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)

                        if msg.content.lower() == 'отмена':
                            await setting.delete()
                            await ctx.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                            try:
                                await msg.delete()
                            except:
                                pass
                            adsp = 0

                        elif msg.content.lower() == '+':
                            newchannel = await ctx.guild.create_text_channel(f'❓┃поддержка', overwrites=None, reason='Создание канала для написани вопросов')
                            one = newchannel.id
                            mesad = await newchannel.send(embed = emb23)
                        else:
                            if "<#" in msg.content.split()[0]:
                                one = msg.content.split()[0].split('#')[1].replace('>', '')
                            else:
                                one = msg.content.split()[0]
                            try:
                                one = int(one)
                            except:
                                await ctx.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                adsp = 0
                                try:
                                    await msg.delete()
                                except:
                                    pass
                            else:
                                if not int(one) in [i.id for i in ctx.guild.text_channels]:
                                    await ctx.send(embed = setembed('✖ Такого канала не существует в данном дискорде!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    adsp = 0
                                if int(one) in [i.id for i in ctx.guild.text_channels]:
                                    try:
                                        await self.bot.get_channel(one).purge(limit = 1000)
                                        mesad = await self.bot.get_channel(one).send(embed = emb23)
                                    except:
                                        pass

                                    try:
                                        await chans.fetch_message(message_id).delete()
                                    except:
                                        pass
                            if adsp != 0:
                                reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"rchannel": one, "channel": one, "message_id": mesad.id}})
                                try:
                                    await msg.delete()
                                except:
                                    pass
                                await ctx.send(embed = setembed(f'✔ Вы успешно установили новый канал для написания вопросов`(`<#{one}>`)`\n`Сообщение от бота уже отправлено в него.`', self.bot.user.avatar_url), delete_after = 5)

                elif str(react.emoji) == '✖':
                    await setting.delete()
                    break

                elif str(react.emoji) == '4⃣':
                    adsp = 1
                    try:
                        await setting.clear_reactions()
                    except:
                        pass
                    await setting.edit(embed = setembed(f'**Укажите новый канал для логирования | Разрешено указывать ID**\n`Для автоматического создания введите` **+**', self.bot.user.avatar_url))
                    def check(m):
                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                    try:
                        msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                    except Exception:
                        return await setting.delete()
                    else:
                        if msg.content.lower() == 'отмена':
                            await setting.delete()
                            await ctx.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                            try:
                                await msg.delete()
                            except:
                                pass
                            adsp = 0

                        elif msg.content.lower() == '+':
                            newchannel2 = await ctx.guild.create_text_channel(f'❕┃логи-репорта', overwrites=None, reason='Создание канала для логирования репорта.')
                            await newchannel2.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                            await newchannel2.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                            one = newchannel2.id
                        else:
                            if "<#" in msg.content.split()[0]:
                                one = msg.content.split()[0].split('#')[1].replace('>', '')
                            else:
                                one = msg.content.split()[0]
                            try:
                                one = int(one)
                            except:
                                await ctx.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                adsp = 0
                                try:
                                    await msg.delete()
                                except:
                                    pass
                            else:
                                if not int(one) in [i.id for i in ctx.guild.text_channels]:
                                    await ctx.send(embed = setembed('✖ Такого канала не существует в данном дискорде!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    adsp = 0
                                if not int(one) in [i.id for i in ctx.guild.text_channels]:
                                    await self.bot.get_channel(one).set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                    await self.bot.get_channel(one).set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                        if not adsp == 0:
                            reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"logchan": one}})
                            try:
                                await msg.delete()
                            except:
                                pass
                            await ctx.send(embed = setembed(f'✔ Вы успешно установили новый канал для логирования репортов`(`<#{one}>`)`.', self.bot.user.avatar_url), delete_after = 5)
                
                elif str(react.emoji) == '3⃣':
                    adsp = 1
                    try:
                        await setting.clear_reactions()
                    except:
                        pass
                    await setting.edit(embed = setembed(f'**Укажите новую роль для агентов технической поддержки этого сервера | Разрешено указывать ID**\n`Для автоматического создания введите` **+**\n\n`Отменить действие можно словом` отмена', self.bot.user.avatar_url))
                    def check(m):
                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                    try:
                        msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                    except Exception:
                        return await setting.delete()
                    else:
                        if msg.content.lower() == 'отмена':
                            await setting.delete()
                            await ctx.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                            try:
                                await msg.delete()
                            except:
                                pass
                            adsp = 0

                        elif msg.content.lower() == '+':
                            newrole = await ctx.guild.create_role(name = '★ Support Team ★', colour = discord.Colour(0x10d30d)) 
                            five = newrole.id
                        else:
                            if "<@&" in msg.content.split()[0]:
                                five = msg.content.split()[0].split('&')[1].replace('>', '')
                            else:
                                five = msg.content.split()[0]
                            try:
                                five = int(five)
                            except:
                                await ctx.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                adsp = 0
                                try:
                                    await msg.delete()
                                except:
                                    pass
                            else:

                                if not int(five) in [i.id for i in ctx.guild.roles]:
                                    await ctx.send(embed = setembed('✖ Такой роли не существует в данном дискорде!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    adsp = 0
                                else:
                                    role = discord.utils.get(ctx.guild.roles, id = rep["support_role"])
                                    for i in role.members:
                                        try:
                                            await i.add_roles(discord.utils.get(ctx.guild.roles, id = five))
                                        except:
                                            pass
                        if not adsp == 0:
                            reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"support_role": five}})
                            try:
                                await msg.delete()
                            except:
                                pass
                            await ctx.send(embed = setembed(f'✔ Вы успешно установили новую роль для технической поддержки Support Team`(`<@&{five}>`)`\n`Новая роль выдана всем предыдущим пользователям с ней.`', self.bot.user.avatar_url), delete_after = 5)

                elif str(react.emoji) == '5⃣':
                    adsp = 1
                    if logged.count_documents({"guild_id": ctx.guild.id}) == 0:
                        logged.insert_one({"guild_id": ctx.guild.id, "voice": 0, "voicechannel": 0, "channels": 0, "channelschannel": 0, "roleedit": 0, "roleeditchannel": 0, "message": 0, "messagechannel": 0, "roleadd": 0, "roleaddchannel": 0, "category": 0})

                    loggeds = logged.find_one({"guild_id": ctx.guild.id})

                    try:
                        await setting.clear_reactions()
                    except:
                        pass
                    for ajkdkwj in range(0, 100):
                        m = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '✖']
                        try:
                            await setting.clear_reactions()
                        except:
                            pass
                        await setting.edit(embed = setembed(f'**Выберите категорию, которую желаете изменить:**\n> 1⃣ - `Включить/выключить логирование сервера`\n> 2⃣ - `Настроить каналы для логирования сервера`\n> 3⃣ - `Установить категорию логирования`\n> 4⃣ - `Автоматическая установка всех логов`\n> 5⃣ - `Полное отключение логов`\n\n> ✖ - `Закрыть меню`', self.bot.user.avatar_url))
                        for i in m:
                            await setting.add_reaction(i)
                        try:
                            react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in m)
                        except Exception:
                            return await setting.delete()
                        else:
                            if str(react.emoji) == '1⃣':
                                adsp = 1
                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                                if loggeds["voice"] == 0:
                                    text1 = f'`Лог действий в голосовых каналах` - Система выключена | ✖'
                                else:
                                    text1 = f'`Лог действий в голосовых каналах` - Система включена | ✔'

                                if loggeds["channels"] == 0:
                                    text2 = f'`Лог действий каналами сервера` - Система выключена | ✖'
                                else:
                                    text2 = f'`Лог действий каналами сервера` - Система включена | ✔'

                                if loggeds["roleedit"] == 0:
                                    text3 = f'`Лог изменений ролей` - Система выключена | ✖'
                                else:
                                    text3 = f'`Лог изменений ролей` - Система включена | ✔'

                                if loggeds["message"] == 0: 
                                    text4 = f'`Логи сообщений` - Система выключена | ✖'
                                else:
                                    text4 = f'`Логи сообщений` - Система включена | ✔'

                                if loggeds["roleadd"] == 0:
                                    text5 = f'`Лог добавления ролей пользователям` - Система выключена | ✖'
                                else:
                                    text5 = f'`Лог добавления ролей пользователям` - Система включена | ✔'

                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                                for asdnakldjawd in range(0, 100):
                                    try:
                                        await setting.clear_reactions()
                                    except:
                                        pass
                                    m = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '✖']
                                    await setting.edit(embed = setembed(f'**Вы попали в меню включения/выключения логирования сервера\n`Выберите необходимый пункт из предложеных:`**\n\n> 1⃣ {text1}\n> 2⃣ {text2}\n> 3⃣ {text3}\n> 4⃣ {text4}\n> 5⃣ {text5}\n\n> ✖ - `Закрыть меню`', self.bot.user.avatar_url))
                                    for i in m:
                                        await setting.add_reaction(i)
                                    try:
                                        react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in m)
                                    except Exception:
                                        return await setting.delete()
                                    else:
                                        if str(react.emoji) == '✖':                            
                                            break

                                        else:
                                            if str(react.emoji) == '1⃣':
                                                ak = 'voice'
                                                if loggeds["voice"] == 0:
                                                    text, af, ac, ar, ad = f'логирование действий в голосовых каналах', 0, 'voicechannel', 'логирования действий в голосовых каналах', '🔸┃Голосовой log'
                                                else:
                                                    text, af, ac, ar, ad = f'логирование действий в голосовых каналах', 1, 'voicechannel', 'логирования действий в голосовых каналах', '🔸┃Голосовой log'
                                            elif str(react.emoji) == '2⃣':
                                                ak = 'channels'
                                                if loggeds["channels"] == 0:
                                                    text, af, ac, ar, ad = f'логирование действий с каналами сервера', 0, 'channelschannel', 'логирования действий с каналами сервера', '🔸┃Каналы log'
                                                else:
                                                    text, af, ac, ar, ad = f'логирование действий с каналами сервера', 1, 'channelschannel', 'логирования действий с каналами сервера', '🔸┃Каналы log'

                                            elif str(react.emoji) == '3⃣':
                                                ak = 'roleedit'
                                                if loggeds["roleedit"] == 0:
                                                    text, af, ac, ar, ad = f'логирование изменений ролей сервера', 0, 'roleeditchannel', 'логирования изменений ролей сервера', '🔸┃Изменение ролей log'
                                                else:
                                                    text, af, ac, ar, ad = f'логирование изменений ролей сервера', 1, 'roleeditchannel', 'логирования изменений ролей сервера', '🔸┃Изменение ролей log'

                                            elif str(react.emoji) == '4⃣':
                                                ak = 'message'
                                                if loggeds["message"] == 0: 
                                                    text, af, ac, ar, ad = f'логирование сообщений', 0, 'messagechannel', 'логирования сообщений', '🔸┃Сообщения log'
                                                else:
                                                    text, af, ac, ar, ad = f'логирование сообщений', 1, 'messagechannel', 'логирования сообщений', '🔸┃Сообщения log'
                                            
                                            elif str(react.emoji) == '5⃣':
                                                ak = 'roleadd'
                                                if loggeds["roleadd"] == 0:
                                                    text, af, ac, ar, ad = f'логирование добавлений ролей пользователям', 0, 'roleaddchannel', 'логирования добавлений ролей пользователям', '🔸┃Добавление ролей log'
                                                else:
                                                    text, af, ac, ar, ad = f'логирование добавлений ролей пользователям', 1, 'roleaddchannel', 'логирования добавлений ролей пользователям', '🔸┃Добавление ролей log'

                                            try:
                                                await setting.clear_reactions()
                                            except:
                                                pass

                                            if af == 0:
                                                if loggeds[ac] == 0:
                                                    try:
                                                        await setting.clear_reactions()
                                                    except:
                                                        pass
                                                    await setting.edit(embed = setembed(f'**Для использования логирования, укажите новый канал для `{ar}` | Разрешено указывать ID**\n`Для автоматического создания введите` **+**\n\n`Отменить действие можно словом` отмена', self.bot.user.avatar_url))
                                                    def check(m):
                                                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                                                    try:
                                                        msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                                                    except Exception:
                                                        return await setting.delete()
                                                    else:
                                                        if msg.content.lower() == 'отмена':
                                                            await ctx.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                                            try:
                                                                await msg.delete()
                                                            except:
                                                                pass
                                                            adsp = 0

                                                        elif msg.content.lower() == '+':
                                                            newchannel2 = await ctx.guild.create_text_channel(f'🔹┃{ad}', overwrites=None, reason= f'Создание канала для {ar}')
                                                            await newchannel2.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                                            await newchannel2.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                                            one = newchannel2.id
                                                        else:
                                                            if "<#" in msg.content.split()[0]:
                                                                one = msg.content.split()[0].split('#')[1].replace('>', '')
                                                            else:
                                                                one = msg.content.split()[0]
                                                            try:
                                                                one = int(one)
                                                            except:
                                                                await ctx.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                                                adsp = 0
                                                                try:
                                                                    await msg.delete()
                                                                except:
                                                                    pass
                                                            else:
                                                                if not int(one) in [i.id for i in ctx.guild.text_channels]:
                                                                    await ctx.send(embed = setembed('✖ Такого канала не существует в данном дискорде!', self.bot.user.avatar_url), delete_after = 5)
                                                                    try:
                                                                        await msg.delete()
                                                                    except:
                                                                        pass
                                                                    adsp = 0
                                                                else:

                                                                    await self.bot.get_channel(one).set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                                                    await self.bot.get_channel(one).set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                                        if adsp != 0:
                                                            logged.update_one({"guild_id": ctx.guild.id}, {"$set": {ac: one, ak: 1}})
                                                            try:
                                                                await msg.delete()
                                                            except:
                                                                pass
                                                            await ctx.send(embed = setembed(f'✔ Вы успешно установили новый канал для {ar}`(`<#{one}>`)`.\nФункция "`{ar}`" успешно активирована.', self.bot.user.avatar_url), delete_after = 5)
                                                else:
                                                    logged.update_one({"guild_id": ctx.guild.id}, {"$set": {ak: 1}})
                                                    await ctx.send(embed = setembed(f'✔ Вы успешно включили функцию "`{text}`".', self.bot.user.avatar_url), delete_after = 5)

                                            else:
                                                logged.update_one({"guild_id": ctx.guild.id}, {"$set": {ak: 0}})
                                                await ctx.send(embed = setembed(f'✔ Вы успешно выключили функцию "`{text}`".', self.bot.user.avatar_url), delete_after = 5)

                            elif str(react.emoji) == '2⃣':
                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                                if logged.find_one({"guild_id": ctx.guild.id})["voicechannel"] == 0:
                                    text1 = 'Не установлен | ✖'
                                else:
                                    text1 = 'Установлен | ✔'

                                if logged.find_one({"guild_id": ctx.guild.id})["channelschannel"] == 0:
                                    text2 = 'Не установлен | ✖'
                                else:
                                    text2 = 'Установлен | ✔'

                                if logged.find_one({"guild_id": ctx.guild.id})["roleeditchannel"] == 0:
                                    text3 = 'Не установлен | ✖'
                                else:
                                    text3 = 'Установлен | ✔'

                                if logged.find_one({"guild_id": ctx.guild.id})["messagechannel"] == 0:
                                    text4 = 'Не установлен | ✖'
                                else:
                                    text4 = 'Установлен | ✔'

                                if logged.find_one({"guild_id": ctx.guild.id})["roleaddchannel"] == 0:
                                    text5 = 'Не установлен | ✖'
                                else:
                                    text5 = 'Установлен | ✔'

                                for adlkmwmd in range(0, 100):
                                    m = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '✖']
                                    adsp = 1
                                    try:
                                        await setting.clear_reactions()
                                    except:
                                        pass
                                    await setting.edit(embed = setembed(f'**Вы попали в меню изменения каналов логирования сервера\n`Выберите необходимый пункт из предложеных:`**\n\n> 1⃣ `Действия в голосовых каналах` - {text1}\n> 2⃣ `Действия с каналами` - {text2}\n> 3⃣ `Действия с изменением ролей` - {text3}\n> 4⃣ `Действия с сообщениями` - {text4}\n> 5⃣ `Действия с добавлением ролей пользователям` - {text5}\n\n> ✖ - `Закрыть меню`', self.bot.user.avatar_url))
                                    for i in m:
                                        await setting.add_reaction(i)
                                    try:
                                        react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in m)
                                    except Exception:
                                        return await setting.delete()
                                    else:
                                        if str(react.emoji) == '✖':                              
                                            break

                                        else:
                                            if str(react.emoji) == '✖':
                                                break

                                            elif str(react.emoji) == '1⃣':
                                                text, ac, ar, ad = f'логирование действий в голосовых каналах', 'voicechannel', 'логирования действий в голосовых каналах', '🔸┃Голосовой log'
                                            elif str(react.emoji) == '2⃣':
                                                text, ac, ar, ad = f'логирование действий с каналами сервера', 'channelschannel', 'логирования действий с каналами сервера', '🔸┃Каналы log'

                                            elif str(react.emoji) == '3⃣':
                                                text, ac, ar, ad = f'логирование изменений ролей сервера', 'roleeditchannel', 'логирования изменений ролей сервера', '🔸┃Изменение ролей log'

                                            elif str(react.emoji) == '4⃣':
                                                text, ac, ar, ad = f'логирование сообщений', 'messagechannel', 'логирования сообщений', '🔸┃Сообщения log'
                                            
                                            elif str(react.emoji) == '5⃣':
                                                text, ac, ar, ad = f'логирование добавлений ролей пользователям', 'roleaddchannel', 'логирования добавлений ролей пользователям', '🔸┃Добавление ролей log'
                                            
                                            try:
                                                await setting.clear_reactions()
                                            except:
                                                pass

                                            await setting.edit(embed = setembed(f'**Укажите новый текстовый канал для `{ar}` | Разрешено указывать ID**\n`Для автоматического создания введите` **+**\n\n`Отменить действие можно словом` отмена', self.bot.user.avatar_url))
                                            def check(m):
                                                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                                            try:
                                                msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                                            except Exception:
                                                return await setting.delete()
                                            else:
                                                if msg.content.lower() == 'отмена':
                                                    await ctx.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                                    try:
                                                        await msg.delete()
                                                    except:
                                                        pass
                                                    adsp = 0

                                                elif msg.content.lower() == '+':
                                                    newchannel2 = await ctx.guild.create_text_channel(f'🔹┃{ad}', overwrites=None, reason= f'Создание канала для {ar}')
                                                    await newchannel2.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                                    await newchannel2.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                                    one = newchannel2.id
                                                else:
                                                    if "<#" in msg.content.split()[0]:
                                                        one = msg.content.split()[0].split('#')[1].replace('>', '')
                                                    else:
                                                        one = msg.content.split()[0]
                                                    try:
                                                        one = int(one)
                                                    except:
                                                        await ctx.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                                        adsp = 0
                                                        try:
                                                            await msg.delete()
                                                        except:
                                                            pass
                                                    else:
                                                        if not int(one) in [i.id for i in ctx.guild.text_channels]:
                                                            await ctx.send(embed = setembed('✖ Такого канала не существует в данном дискорде!', self.bot.user.avatar_url), delete_after = 5)
                                                            try:
                                                                await msg.delete()
                                                            except:
                                                                pass
                                                            adsp = 0
                                                        else:

                                                            await self.bot.get_channel(one).set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                                            await self.bot.get_channel(one).set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                                                if adsp != 0:
                                                    logged.update_one({"guild_id": ctx.guild.id}, {"$set": {ac: one}})
                                                    try:
                                                        await msg.delete()
                                                    except:
                                                        pass
                                                    await ctx.send(embed = setembed(f'✔ Вы успешно установили новый канал для {ar}`(`<#{one}>`)`.', self.bot.user.avatar_url), delete_after = 5)

                            elif str(react.emoji) == '3⃣':
                                adsp = 1
                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                                await setting.edit(embed = setembed(f'**Введите ID категории, в которой будут находиться log-каналы | Для автоматического создания введите `+`**\n\n`Отменить действие можно словом` отмена', self.bot.user.avatar_url))
                                def check(m):
                                    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                                try:
                                    msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                                except Exception:
                                    return await setting.delete()
                                else:
                                    if msg.content.lower() == 'отмена':
                                        await ctx.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                        try:
                                            await msg.delete()
                                        except:
                                            pass
                                        adsp = 0

                                    elif msg.content.lower() == '+':
                                        newcat1 = await ctx.guild.create_category(name = 'Логирование', reason='Создание катигории для log-каналов')
                                        await newcat1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                        await newcat1.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                    else:
                                        try:
                                            ct = int(msg.content.split()[0])
                                        except:
                                            await ctx.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                            adsp = 0
                                            try:
                                                await msg.delete()
                                            except:
                                                pass
                                        else:

                                            if not int(ct) in [i.id for i in ctx.guild.categories]:
                                                await ctx.send(embed = setembed('✖ Такой категории не существует в данном дискорде. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 10)
                                                try:
                                                    await msg.delete()
                                                except:
                                                    pass
                                                adsp = 0
                                            else:
                                                newcat1 = discord.utils.get(ctx.guild.categories, id = ct)
                                                await newcat1.edit(name = 'Логирование')
                                                await newcat1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                                await newcat1.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                    
                                    if adsp != 0:
                                        categ = discord.utils.get(ctx.guild.categories, id = newcat1.id)
                                        loggeds = logged.find_one({"guild_id": ctx.guild.id})
                                        try:
                                            if loggeds["voicechannel"] > 1:
                                                await self.bot.get_channel(loggeds["voicechannel"]).edit(category = categ)
                                        except:
                                            pass

                                        try:
                                            if loggeds["channelschannel"] > 1:
                                                await self.bot.get_channel(loggeds["channelschannel"]).edit(category = categ)
                                        except:
                                            pass

                                        try:
                                            if loggeds["roleeditchannel"] > 1:
                                                await self.bot.get_channel(loggeds["roleeditchannel"]).edit(category = categ)
                                        except:
                                            pass

                                        try:
                                            if loggeds["messagechannel"] > 1:
                                                await self.bot.get_channel(loggeds["messagechannel"]).edit(category = categ)
                                        except:
                                            pass

                                        try:
                                            if loggeds["roleaddchannel"] > 1:
                                                await self.bot.get_channel(loggeds["roleaddchannel"]).edit(category = categ)
                                        except:
                                            pass

                                        logged.update_one({"guild_id": ctx.guild.id}, {"$set": {"category": categ.id}})
                                        try:
                                            await msg.delete()
                                        except:
                                            pass
                                        await ctx.send(embed = setembed(f'✔ Отлично, теперь log-каналы будут попадать в категорию `({categ.name} | {categ.id})`\n`[P.S]: Старые log-каналы были перемещены в новую категорию.`', self.bot.user.avatar_url), delete_after = 5)

                            elif str(react.emoji) == '4⃣':
                                m = ['1⃣', '2⃣', '✖']
                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                                await setting.edit(embed = setembed(f'**Выберите интересующий Вас пункт:**\n> 1⃣ - `Включить логирование с заменой существующих каналов`\n> 2⃣ - `Включить логирование без замены существующих каналов`\n\n> ✖ - `Закрыть меню`', self.bot.user.avatar_url))
                                for i in m:
                                    await setting.add_reaction(i)
                                try:
                                    react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in m)
                                except Exception:
                                    return await setting.delete()
                                else:
                                    try:
                                        await setting.clear_reactions()
                                    except:
                                        pass
                                    if str(react.emoji) == '1⃣':
                                        if loggeds["category"] == 0:
                                            newcat1 = await ctx.guild.create_category(name = 'Логирование', reason='Создание катигории для log-каналов')
                                            await newcat1.edit(name = 'Логирование')
                                            await newcat1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                            await newcat1.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                        else:
                                            newcat1 = discord.utils.get(ctx.guild.categories, id = loggeds["category"])

                                        if loggeds["voicechannel"] == 0:
                                            newchannel1 = await ctx.guild.create_text_channel(f'🔸┃Голосовой log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования действий в голосовых каналах')
                                            await newchannel1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                            await newchannel1.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                        else:
                                            newchannel1 = self.bot.get_channel(loggeds["voicechannels"])
                                            await newchannel1.edit(category = newcat1)

                                        if loggeds["channelschannel"] == 0:
                                            newchannel2 = await ctx.guild.create_text_channel(f'🔸┃Каналы log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования действий с каналами сервера')
                                            await newchannel2.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                            await newchannel2.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                        else:
                                            newchannel2 = self.bot.get_channel(loggeds["channelschannel"])
                                            await newchannel2.edit(category = newcat1)

                                        if loggeds["roleeditchannel"] == 0:
                                            newchannel3 = await ctx.guild.create_text_channel(f'🔸┃Изменение ролей log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования изменений ролей сервера')
                                            await newchannel3.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                            await newchannel3.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                        else:
                                            newchannel3 = self.bot.get_channel(loggeds["roleeditchannel"])
                                            await newchannel3.edit(category = newcat1)

                                        if loggeds["messagechannel"] == 0:
                                            newchannel4 = await ctx.guild.create_text_channel(f'🔸┃Сообщения log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования сообщений')
                                            await newchannel4.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                            await newchannel4.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                        else:
                                            newchannel4 = self.bot.get_channel(loggeds["messagechannel"])
                                            await newchannel4.edit(category = newcat1)
                                        
                                        if loggeds["roleaddchannel"] == 0:
                                            newchannel5 = await ctx.guild.create_text_channel(f'🔸┃Добавление ролей log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования добавлений ролей пользователям')
                                            await newchannel5.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                            await newchannel5.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                        else:
                                            newchannel5 = self.bot.get_channel(loggeds["roleaddchannel"])
                                            await newchannel5.edit(category = newcat1)

                                        logged.update_one({"guild_id": ctx.guild.id}, {"$set": {"voice": 1, "voicechannel": newchannel1.id, "channels": 1, "channelschannel": newchannel2.id, "roleedit": 1, "roleeditchannel": newchannel3.id, "message": 1, "messagechannel": newchannel4.id, "roleadd": 1, "roleaddchannel": newchannel5.id}})
                                        await ctx.send(embed = setembed(f'✔ Вы успешно установили систему логирования без замены старых каналов:\n> 🔺 `Категория логирования:` {newcat1.name}`(ID: {newcat1.id})`\n> 🔹 `Канал голосового логирования:` <#{newchannel1.id}>`(ID: {newchannel1.id})`\n> 🔹 `Канал логирования изменений каналов:` <#{newchannel2.id}>`(ID: {newchannel2.id})`\n> 🔹 `Канал логирования изменения ролей:` <#{newchannel3.id}>`(ID: {newchannel3.id})`\n> 🔹 `Канал логирования сообщений:` <#{newchannel4.id}>`(ID: {newchannel4.id})`\n> 🔹 `Канал логирования добавления ролей пользователям:` <#{newchannel5.id}>`(ID: {newchannel5.id})`', self.bot.user.avatar_url), delete_after = 5)
                                    
                                    elif str(react.emoji) == '2⃣':
                                        if loggeds["category"] == 0:
                                            newcat1 = await ctx.guild.create_category(name = 'Логирование', reason='Создание катигории для log-каналов')
                                            await newcat1.edit(name = 'Логирование')
                                            await newcat1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                            await newcat1.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                        else:
                                            newcat1 = discord.utils.get(ctx.guild.categories, id = loggeds["category"])

                                        newchannel1 = await ctx.guild.create_text_channel(f'🔸┃Голосовой log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования действий в голосовых каналах')
                                        await newchannel1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                        await newchannel1.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                                        newchannel2 = await ctx.guild.create_text_channel(f'🔸┃Каналы log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования действий с каналами сервера')
                                        await newchannel2.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                        await newchannel2.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                                        newchannel3 = await ctx.guild.create_text_channel(f'🔸┃Изменение ролей log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования изменений ролей сервера')
                                        await newchannel3.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                        await newchannel3.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                                        newchannel4 = await ctx.guild.create_text_channel(f'🔸┃Сообщения log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования сообщений')
                                        await newchannel4.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                        await newchannel4.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                        
                                        newchannel5 = await ctx.guild.create_text_channel(f'🔸┃Добавление ролей log', category = newcat1, overwrites=None, reason= f'Создание канала для логирования добавлений ролей пользователям')
                                        await newchannel5.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                        await newchannel5.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                                        logged.update_one({"guild_id": ctx.guild.id}, {"$set": {"voice": 1, "voicechannel": newchannel1.id, "channels": 1, "channelschannel": newchannel2.id, "roleedit": 1, "roleeditchannel": newchannel3.id, "message": 1, "messagechannel": newchannel4.id, "roleadd": 1, "roleaddchannel": newchannel5.id}})
                                        await ctx.send(embed = setembed(f'✔ Вы успешно установили чистую систему логирования:\n> 🔺 `Категория логирования:` {newcat1.name}`(ID: {newcat1.id})`\n> 🔹 `Канал голосового логирования:` <#{newchannel1.id}>`(ID: {newchannel1.id})`\n> 🔹 `Канал логирования изменений каналов:` <#{newchannel2.id}>`(ID: {newchannel2.id})`\n> 🔹 `Канал логирования изменения ролей:` <#{newchannel3.id}>`(ID: {newchannel3.id})`\n> 🔹 `Канал логирования сообщений:` <#{newchannel4.id}>`(ID: {newchannel4.id})`\n> 🔹 `Канал логирования добавления ролей пользователям:` <#{newchannel5.id}>`(ID: {newchannel5.id})`', self.bot.user.avatar_url), delete_after = 5)

                                    elif str(react.emoji) == '✖':
                                        await setting.delete()
                                        break

                            elif str(react.emoji) == '5⃣':
                                m = ['1⃣', '2⃣', '✖']
                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                                await setting.edit(embed = setembed(f'**Выберите интересующий Вас пункт:**\n> 1⃣ - `Выключить и удалить log-каналы`\n> 2⃣ - `Выключить без удаления log-каналов`\n\n> ✖ - `Закрыть меню`', self.bot.user.avatar_url))
                                for i in m:
                                    await setting.add_reaction(i)
                                try:
                                    react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in m)
                                except Exception:
                                    return await setting.delete()
                                else:
                                    try:
                                        await setting.clear_reactions()
                                    except:
                                        pass
                                    if str(react.emoji) == '1⃣':
                                        loggeds = logged.find_one({"guild_id": ctx.guild.id})
                                        try:
                                            if loggeds["voicechannel"] > 1:
                                                await self.bot.get_channel(loggeds["voicechannel"]).delete()
                                        except:
                                            pass

                                        try:
                                            if loggeds["channelschannel"] > 1:
                                                await self.bot.get_channel(loggeds["channelschannel"]).delete()
                                        except:
                                            pass

                                        try:
                                            if loggeds["roleeditchannel"] > 1:
                                                await self.bot.get_channel(loggeds["roleeditchannel"]).delete()
                                        except:
                                            pass

                                        try:
                                            if loggeds["messagechannel"] > 1:
                                                await self.bot.get_channel(loggeds["messagechannel"]).delete()
                                        except:
                                            pass

                                        try:
                                            if loggeds["roleaddchannel"] > 1:
                                                await self.bot.get_channel(loggeds["roleaddchannel"]).delete()
                                        except:
                                            pass
                                        
                                        cat = loggeds["category"]
                                        logged.delete_one({"guild_id": ctx.guild.id})
                                        logged.insert_one({"guild_id": ctx.guild.id, "voice": 0, "voicechannel": 0, "channels": 0, "channelschannel": 0, "roleedit": 0, "roleeditchannel": 0, "message": 0, "messagechannel": 0, "roleadd": 0, "roleaddchannel": 0, "category": cat})
                                        await ctx.send(embed = setembed(f'✔ Вы успешно удалили все log-каналы\n`[P.S]: Система логирования полностью отключена.`', self.bot.user.avatar_url), delete_after = 5)
                                    elif str(react.emoji) == '2⃣':
                                        logged.update_one({"guild_id": ctx.guild.id}, {"$set": {"voice": 0, "message": 0, "roleedit": 0, "channels": 0, "roleadd": 0}})
                                        await ctx.send(embed = setembed(f'✔ Вы успешно отключили всю систему логирования.\n\n❤ `Спасибо что используете именно меня!`', self.bot.user.avatar_url), delete_after = 5)
                                    elif str(react.emoji) == '✖':
                                        await setting.delete()
                                        break

                            elif str(react.emoji) == '✖':
                                await setting.delete()
                                break
                
                elif str(react.emoji) == '6⃣':
                    try:
                        await setting.clear_reactions()
                    except:
                        pass
                    if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 3}) == 0:
                        reports.insert_one({"guild_id": ctx.guild.id, "proverka": 3, "sender": 1, "ocenka": 1})
                    for ajkdkwj in range(0, 100):
                        m = ['1⃣', '2⃣', '✖']
                        try:
                            await setting.clear_reactions()
                        except:
                            pass
                        if reports.find_one({"guild_id": ctx.guild.id, "proverka": 3})["sender"] == 1:
                            text1 = '`Включить систему принятия репорта` | Сейчас включена ✔'
                            text2 = '`Выключить систему принятия репорта`'
                        else:
                            text2 = '`Выключить систему принятия репорта` | Сейчас выключена ✖'
                            text1 = '`Включить систему принятия репорта`'
                        await setting.edit(embed = setembed(f'**Выберите категорию, которую желаете изменить:**\n> 1⃣ - {text1}\n> 2⃣ - {text2}\n\n> ✖ - `Закрыть меню`', self.bot.user.avatar_url))
                        for i in m:
                            await setting.add_reaction(i)
                        try:
                            react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in m)
                        except Exception:
                            return await setting.delete()
                        else:
                            if str(react.emoji) == '1⃣':
                                if reports.find_one({"guild_id": ctx.guild.id, "proverka": 3})["sender"] == 1:
                                    await ctx.send(embed = setembed(f'✔ Система "`Принятие репорта`" уже включена.', self.bot.user.avatar_url), delete_after = 5)
                                else:
                                    reports.update_one({"guild_id": ctx.guild.id, "proverka": 3}, {"$set": {"sender": 1}})
                                    await ctx.send(embed = setembed(f'✔ Вы успешно включили систему "`Принятие репорта`"\n`[P.S]: Принимать репорты необходимо в канале` <#{rep["logchan"]}>', self.bot.user.avatar_url), delete_after = 10)
                            elif str(react.emoji) == '2⃣':
                                if reports.find_one({"guild_id": ctx.guild.id, "proverka": 3})["sender"] == 0:
                                    await ctx.send(embed = setembed(f'✔ Система "`Принятие репорта`" не включена.', self.bot.user.avatar_url), delete_after = 5)
                                else:
                                    reports.update_one({"guild_id": ctx.guild.id, "proverka": 3}, {"$set": {"sender": 0}})
                                    await ctx.send(embed = setembed(f'✔ Вы успешно выключили систему "`Принятие репорта`"\n`[P.S]: Теперь на репорт может отвечать каждый агент технической поддержки с ролью` <@&{rep["support_role"]}>', self.bot.user.avatar_url), delete_after = 10)
                            elif str(react.emoji) == '✖':
                                await setting.delete()
                                break

                elif str(react.emoji) == '7⃣':
                    try:
                        await setting.clear_reactions()
                    except:
                        pass
                    if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 3}) == 0:
                        reports.insert_one({"guild_id": ctx.guild.id, "proverka": 3, "sender": 1, "ocenka": 1})
                    for ajkdkwj in range(0, 100):
                        m = ['1⃣', '2⃣', '✖']
                        try:
                            await setting.clear_reactions()
                        except:
                            pass
                        if reports.find_one({"guild_id": ctx.guild.id, "proverka": 3})["ocenka"] == 1:
                            text1 = '`Включить систему оценки ответа модератора` | Сейчас включена ✔'
                            text2 = '`Выключить систему оценки ответа модератора`'
                        else:
                            text2 = '`Выключить систему оценки ответа модератора` | Сейчас выключена ✖'
                            text1 = '`Включить систему оценки ответа модератора`'
                        await setting.edit(embed = setembed(f'**Выберите категорию, которую желаете изменить:**\n> 1⃣ - {text1}\n> 2⃣ - {text2}\n\n> ✖ - `Закрыть меню`', self.bot.user.avatar_url))
                        for i in m:
                            await setting.add_reaction(i)
                        try:
                            react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in m)
                        except Exception:
                            return await setting.delete()
                        else:
                            if str(react.emoji) == '1⃣':
                                if reports.find_one({"guild_id": ctx.guild.id, "proverka": 3})["ocenka"] == 1:
                                    await ctx.send(embed = setembed(f'✔ Система "`Оценка ответа модератора`" уже включена.', self.bot.user.avatar_url), delete_after = 5)
                                else:
                                    reports.update_one({"guild_id": ctx.guild.id, "proverka": 3}, {"$set": {"ocenka": 1}})
                                    await ctx.send(embed = setembed(f'✔ Вы успешно включили систему "`Оценка ответа модератора`"\n`[P.S]: Теперь человек создавший вопрос, сможет оценить ответ модератора`', self.bot.user.avatar_url), delete_after = 10)
                            elif str(react.emoji) == '2⃣':
                                if reports.find_one({"guild_id": ctx.guild.id, "proverka": 3})["ocenka"] == 0:
                                    await ctx.send(embed = setembed(f'✔ Система "`Оценка ответа модератора`" не включена.', self.bot.user.avatar_url), delete_after = 5)
                                else:
                                    reports.update_one({"guild_id": ctx.guild.id, "proverka": 3}, {"$set": {"ocenka": 0}})
                                    await ctx.send(embed = setembed(f'✔ Вы успешно выключили систему "`Оценка ответа модератора`"\n`[P.S]: Теперь пользователи не смогут оценивать ответы модераторов`', self.bot.user.avatar_url), delete_after = 10)
                            elif str(react.emoji) == '✖':
                                await setting.delete()
                                break

                elif str(react.emoji) == '2⃣':
                    try:
                        await setting.clear_reactions()
                    except:
                        pass
                    for ajsdnkjad in range(0, 100):
                        m = ['1⃣', '2⃣', '3⃣', '✖']
                        adsp = 1
                        try:
                            await setting.clear_reactions()
                        except:
                            pass
                        await setting.edit(embed = setembed(f'**Выберите категорию, которую желаете изменить:**\n> 1⃣ - `Активные вопросы`\n> 2⃣ - `Вопросы на рассмотрении`\n> 3⃣ - `Закрытые вопросы(Корзина)`\n\n> ✖ - `Закрыть меню`', self.bot.user.avatar_url))
                        for i in m:
                            await setting.add_reaction(i)
                        try:
                            react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == ctx.author and react.message.channel == ctx.channel and react.emoji in m)
                        except Exception:
                            return await setting.delete()
                        else:
                            if str(react.emoji) == '1⃣':
                                af, cname = "category_id_one", "Активные вопросы"
                                ar = 'активные вопросы'
                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                            elif str(react.emoji) == '2⃣':
                                af, cname = "category_id_two", "На рассмотрении"
                                ar = 'вопросы находящиеся на рассмотрении'
                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                            elif str(react.emoji) == '3⃣':
                                af, cname = "category_id_three", "Корзина"
                                ar = 'закрытые вопросы(Корзина)'
                                try:
                                    await setting.clear_reactions()
                                except:
                                    pass
                            elif str(react.emoji) == '✖':
                                await setting.delete()
                                break
                            try:
                                await setting.clear_reactions()
                            except:
                                pass
                            await setting.edit(embed = setembed(f'**Введите ID категории, в которой будут находиться `{ar}`**\n`Для автоматического создания введите` **+**\n\n`Отменить действие можно словом` отмена', self.bot.user.avatar_url))
                            def check(m):
                                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                            try:
                                msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                            except Exception:
                                return await setting.delete()
                            else:
                                if msg.content.lower() == 'отмена':
                                    await ctx.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    adsp = 0

                                elif msg.content.lower() == '+':
                                    newcat1 = await ctx.guild.create_category(name = cname, reason='Создание катигории для активных вопросов')
                                    if cname == "Корзина":
                                        await newcat1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                    else:
                                        await newcat1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = True, read_message_history = True)
                                    await newcat1.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                else:
                                    try:
                                        ct = int(msg.content.split()[0])
                                    except:
                                        await ctx.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                        adsp = 0
                                        try:
                                            await msg.delete()
                                        except:
                                            pass
                                    else:
                                        if not int(ct) in [i.id for i in ctx.guild.categories]:
                                            await ctx.send(embed = setembed('✖ Такой категории не существует в данном дискорде. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 10)
                                            try:
                                                await msg.delete()
                                            except:
                                                pass
                                            adsp = 0
                                        else:
                                            newcat1 = discord.utils.get(ctx.guild.categories, id = ct)
                                            await newcat1.edit(name = cname)
                                            if cname == "Корзина":
                                                await newcat1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = False, read_message_history = True)
                                            else:
                                                await newcat1.set_permissions(discord.utils.get(ctx.guild.roles, id = rep["support_role"]), read_messages = True, send_messages = True, read_message_history = True)
                                            await newcat1.set_permissions(ctx.guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                                
                                if adsp != 0:
                                    categ = discord.utils.get(ctx.guild.categories, id = newcat1.id)
                                    reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {af: newcat1.id}})
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await ctx.send(embed = setembed(f'✔ Отлично, теперь {ar} будут попадать в категорию `({categ.name} | {categ.id})`\n', self.bot.user.avatar_url), delete_after = 5)

    @commands.command(aliases = ["ver"])
    @commands.is_owner()
    async def verificated(self, ctx, id = None):
        if ctx.guild == None:
            return

        await ctx.message.delete()

        if id == None or id == '-':
            gid = ctx.guild.id

        try:
            guild = self.bot.get_guild(gid)
            name = guild.name
        except:
            return await ctx.send(embed = setembed(f'✖ Указаной гильдии не существует', self.bot.user.avatar_url), delete_after = 5)

        if reports.count_documents({"guild_id": gid, "proverka": 1}) == 0:
            return await ctx.send(embed = setembed(f'✖ Указаная гильдия не зарегистрирована в базе данных.', self.bot.user.avatar_url), delete_after = 5)

        if id == '-':
            if reports.find_one({"guild_id": gid, "proverka": 1})["donate"] == 0:
                return await ctx.send(embed = setembed(f'✖ Сервер `{guild.name}` не верифицирован', self.bot.user.avatar_url), delete_after = 5)
            else:
                return await ctx.send(embed = setembed(f'✔ Сервер `{guild.name}` верифицирован', self.bot.user.avatar_url), delete_after = 5)

        if reports.find_one({"guild_id": gid, "proverka": 1})["donate"] == 1:
            value = 1
        else:
            value = 0

        if value == 0:
            message = await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы действительно хотите верифицировать гильдию `{guild.name}`?\n\n> ❤ `- Да`\n> 💔 `- Нет`', colour = 0xFB9E14))
            await message.add_reaction('❤')
            await message.add_reaction('💔')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['💔', '❤'])
            except Exception:
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '💔':
                    return
                elif str(react.emoji) == '❤':
                    await ctx.send(embed = setembed(f'Сервер `{guild.name}` успешно верифицирован.', self.bot.user.avatar_url), delete_after = 15)
                    try:
                        await guild.owner.send(embed = setembed(f'✔ Ваш сервер `{guild.name}` успешно верифицирован.\n\nТеперь Вам доступны такие функции как:\n> `Принятие репорта отдельным человеком`\n> `Логгирования действий в дискорде`\n> `Люди смогут оценивать ответ модератора`\nВсё это Вы сможете настроить в меню `!settings` в Вашем дискорд-сервере.\nПосмотреть статистику модератора: `!imoder @Пользователь#1234`\n\n**Спасибо что используете меня!**', self.bot.user.avatar_url))
                    except:
                        pass
                    reports.insert_one({"guild_id": guild.id, "proverka": 3, "sender": 1, "ocenka": 1})
                    reports.update_one({"guild_id": guild.id, "proverka": 1}, {"$set": {"donate": 1}})
        else:
            await ctx.send(embed = setembed(f'С сервера `{guild.name}` успешно снята верификация.', self.bot.user.avatar_url), delete_after = 15)
            try:
                await guild.owner.send(embed = setembed(f'✖ Ваш сервер `{guild.name}` был удалён из списка верифицированных серверов бота.\n\nТеперь Вам не доступны такие функции как:\n> `Принятие репорта отдельным человеком`\n> `Логгирования действий в дискорде`\n> `Люди не смогут оценивать ответ модератора`\nКоманда просмотра статистики модератора отключена', self.bot.user.avatar_url))
            except:
                pass
            reports.update_one({"guild_id": guild.id, "proverka": 1}, {"$set": {"donate": 0}})
            reports.delete_one({"guild_id": guild.id, "proverka": 3})
        
    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def setfooter(self, ctx, *, text: str = None):
        if ctx.guild == None:
            return

        if not reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 1:
            return

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})
        if rep["start_channel"] > 0:
            return await ctx.send(embed = setembed(f'Для начала работы со мной, необходимо пройти регистрацию в базе данных.\n`Закончите регистрацию в канале` <#{rep["start_channel"]}>\n\n**Если произошла ошибка и необходимо пройти регистрацию заново, введите `!reload`**', self.bot.user.avatar_url), delete_after = 10)

        if ctx.channel.id == rep["rchannel"]:
            return

        await ctx.message.delete()

        if text == None:
            return await ctx.send(embed = setembed(f'Для установки подписи, мне необходимо знать её текст.\n\n`Пример использования команды:`\n> !setfooter Прекрасного дня и хорошего настроения!\n`-- Я установлю в report-сообщение (сообщение в канале с новым репортом) подпись:` Прекрасного дня и хорошего настроения!\n\n> !setfooter -\n`-- Я подпись автора под сообщением `(Support Team by {reports.find_one({"proverka": 2})["discord"]})\n\n> **Длинна подписи не должна превышать `80` символов.**', self.bot.user.avatar_url), delete_after = 10)

        if text.lower() == '-':
            reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"footer": "None"}})
            await ctx.send(embed = setembed(f'✔ Установлена моя личная подпись:\n`Support Team by {reports.find_one({"proverka": 2})["discord"]}`', self.bot.user.avatar_url), delete_after = 5)
        else:
            if len(list(text)) > 80:
                return await ctx.send(embed = setembed(f'✖ Длинна подписи не должна быть больше 80-ти символов.', self.bot.user.avatar_url), delete_after = 5)
            else:
                reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"footer": text}})
                return await ctx.send(embed = setembed(f'✔ Установлена моя личная подпись:\n`{text}`', self.bot.user.avatar_url), delete_after = 5)
    
    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def sethimes(self, ctx, *, text: str = None):
        if ctx.guild == None:
            return

        if not reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 1:
            return

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})
        if rep["start_channel"] > 0:
            return await ctx.send(embed = setembed(f'Для начала работы со мной, необходимо пройти регистрацию в базе данных.\n`Закончите регистрацию в канале` <#{rep["start_channel"]}>\n\n**Если произошла ошибка и необходимо пройти регистрацию заново, введите `!reload`**', self.bot.user.avatar_url), delete_after = 10)

        if ctx.channel.id == rep["rchannel"]:
            return

        await ctx.message.delete()

        if text == None:
            return await ctx.send(embed = setembed(f'Для установки фантомного сообщения после репорта, мне необходимо знать его текст.\n\n`Пример использования команды:`\n> !sethimes Прекрасного дня и хорошего настроения!\n`-- Я установлю фантомным (пропадающим через 30 секунд) сообщением:` Прекрасного дня и хорошего настроения!\n\n> !setfooter -\n`-- Я не буду отправлять фантомное сообщение.`\n\n> **Длинна фантомного сообщения не должна превышать `150` символов.**', self.bot.user.avatar_url), delete_after = 10)

        if text.lower() == '-':
            reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"himes": "None"}})
            await ctx.send(embed = setembed(f'✔ Фантомное сообщение отключено.', self.bot.user.avatar_url), delete_after = 5)
        else:
            if len(list(text)) > 150:
                return await ctx.send(embed = setembed(f'✖ Фантомное сообщение не должно быть больше 150-ти символов.', self.bot.user.avatar_url), delete_after = 5)
            else:
                reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"himes": text}})
                return await ctx.send(embed = setembed(f'✔ Установлено новое фантомное сообщение:\n\n"`{text}`"', self.bot.user.avatar_url), delete_after = 5)

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def setimage(self, ctx, url: str = None):
        if ctx.guild == None:
            return

        mas = ["https://static.tildacdn.com/tild3838-3366-4433-a161-333932353933/banner3.png", "https://arcnet.pro/upload/iblock/71f/71f38734b69026df6075aae27169a289.jpg", "https://s3.ap-south-1.amazonaws.com/townscript-production/images/158322568658636913c83-7735-4f7e-9200-d9be2d5ad648.png", "https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif"]

        if not reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 1:
            return

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})
        if rep["start_channel"] > 0:
            return await ctx.send(embed = setembed(f'Для начала работы со мной, необходимо пройти регистрацию в базе данных.\n`Закончите регистрацию в канале` <#{rep["start_channel"]}>\n\n**Если произошла ошибка и необходимо пройти регистрацию заново, введите `!reload`**', self.bot.user.avatar_url), delete_after = 10)

        if ctx.channel.id == rep["rchannel"]:
            return

        await ctx.message.delete()

        if url == None:
            return await ctx.send(embed = setembed(f'Для установки изображения мне необходима прямая ссылка на него.\n\n`Пример использования команды:`\n> !setimage https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif\n`-- Я установлю в изначальное сообщение изображение по Вашей ссылке.`\n\n> !setimage -\n`-- Я установлю свою картинку в изначальное сообщение.`', self.bot.user.avatar_url), delete_after = 10)

        if url.lower() == '-':
            reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"image": random.choice(mas)}})
            await ctx.send(embed = setembed(f'✔ Изображение успешно установлено.', self.bot.user.avatar_url), delete_after = 5)

        else:
            if not 'https://' in url:
                return await ctx.send(embed = setembed(f'Для установки изображения в изначальное сообщение, Вам необходимо заполнить поле "Ссылка".\n\n`Пример использования команды:`\n> !setimage https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif\n`-- Я установлю в изначальное сообщение изображение по Вашей ссылке.`\n\n> !setimage -\n`-- Я установлю свою картинку в изначальное сообщение.`', self.bot.user.avatar_url), delete_after = 10)

            reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"image": url}})
            await ctx.send(embed = setembed(f'✔ Изображение успешно установлено.\n> `Ссылка а изображение:` {url}', self.bot.user.avatar_url), delete_after = 5)

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})
        message_id = rep["message_id"]
        chans = self.bot.get_channel(rep["channel"])
        message = await chans.fetch_message(message_id)
        emb23 = discord.Embed(description = f'Доброго времени суток! Вы попали в канал технической поддержки сервера **{ctx.guild.name}**\nТут Вы можете узнать, как получить техническую поддержку от наших модераторов <@&{rep["support_role"]}>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
        emb23.set_author(name=f'{ctx.guild.name} | Support', icon_url= 'https://mydovidka.com/wp-content/uploads/2019/11/de0e202e9992854eade6f1ddf73dff49.png')
        emb23.add_field(name = 'Правила создания репорта', value = '```> Запрещены сообщения не несущие информации или вопроса.\n> Запрещено использовать ненормативную лексику.\n> Запрещено флудить @упоминаниями.\n> Запрещено создавать репорт с некорректным вопросом.\n> Запрещено оскорбительное и неадекватное поведение.\n> Для того что бы задать вопрос, вам необходимо написать его в этот канал.```', inline = False)
        emb23.add_field(name = 'Общее количество', value='\n'f'**⚙** `{rep["vsego"]}` вопросов', inline = True)
        emb23.add_field(name = 'На рассмотрении', value = f'**⚙** `{rep["active"]}` вопросов', inline = True)
        emb23.add_field(name = 'Обработано', value = f'**⚙** `{rep["close"]}` вопросов\n', inline=True)
        emb23.add_field(name = 'Последний вопрос от:', value=f'`{ctx.author.display_name}`', inline = False)
        if rep["image"] == "None":
            emb23.set_image(url= 'https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif')
        else:
            emb23.set_image(url= rep["image"])
        emb23.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
        emb23.set_thumbnail(url= ctx.guild.icon_url)
        return await message.edit(embed=emb23)

    @commands.command()
    async def on_member_remove(self, member):
        if reports.count_documents({"guild_id": member.guild.id, "user_id": member.id}) == 1:
            try:
                await member.guild.get_channel(reports.find_one({"guild_id": member.guild.id, "user_id": member.id})["rep_chat"]).delete()
            except:
                pass
            reports.delete_one({"guild_id": member.guild.id, "user_id": member.id})
            rep = reports.find_one({"guild_id": member.guild.id, "user_id": member.id})
            x = int(rep["close"]) + 1
            y = int(rep["active"]) - 1
            reports.update_one({"proverka": 1, "guild_id": member.guild.id}, {"$set": {"close": x, "active": y, "last_name": 'dollar ム baby#3603'}})
            message_id = rep["message_id"]
            chans = self.bot.get_channel(rep["channel"])
            message = await chans.fetch_message(message_id)
            emb23 = discord.Embed(description = f'Доброго времени суток! Вы попали в канал технической поддержки сервера **{member.guild.name}**\nТут Вы можете узнать, как получить техническую поддержку от наших модераторов <@&{rep["support_role"]}>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
            emb23.set_author(name=f'{member.guild.name} | Support', icon_url= 'https://mydovidka.com/wp-content/uploads/2019/11/de0e202e9992854eade6f1ddf73dff49.png')
            emb23.add_field(name = 'Правила создания репорта', value = '```> Запрещены сообщения не несущие информации или вопроса.\n> Запрещено использовать ненормативную лексику.\n> Запрещено флудить @упоминаниями.\n> Запрещено создавать репорт с некорректным вопросом.\n> Запрещено оскорбительное и неадекватное поведение.\n> Для того что бы задать вопрос, вам необходимо написать его в этот канал.```', inline = False)
            emb23.add_field(name = 'Общее количество', value='\n'f'**⚙** `{rep["vsego"]}` вопросов', inline = True)
            emb23.add_field(name = 'На рассмотрении', value = f'**⚙** `{y}` вопросов', inline = True)
            emb23.add_field(name = 'Обработано', value = f'**⚙** `{x}` вопросов\n', inline=True)
            emb23.add_field(name = 'Последний вопрос от:', value=f'`dollar ム baby#3603`', inline = False)
            if rep["image"] == "None":
                emb23.set_image(url= 'https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif')
            else:
                emb23.set_image(url= rep["image"])
            emb23.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
            emb23.set_thumbnail(url= member.guild.icon_url)
            await message.edit(embed=emb23)

    @commands.command(aliases = ['привет', 'hello', 'хай', 'хеллоу', 'ку', 'qq']) 
    async def hi(self, ctx): 
        if ctx.guild == None:
            return

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})

        role = discord.utils.get(ctx.guild.roles, id = rep["support_role"]) 
        if not role in ctx.author.roles: 
            return 

        await ctx.message.delete() 
        embed = discord.Embed(color = 0xFB9E14) 
        embed.set_footer(text = f'Ответ был дан модератором {ctx.author.display_name}', icon_url = self.bot.user.avatar_url) 
        return await ctx.send(f'`[MODERATOR] Здравствуйте, я агент технической поддержки - {ctx.author.display_name}, я постараюсь помочь Вам в решении вашей проблемы.`', embed = embed) 

    @commands.command(aliases = ['пока', 'bb', 'бб']) 
    async def by(self, ctx): 
        if ctx.guild == None:
            return

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})

        role = discord.utils.get(ctx.guild.roles, id = rep["support_role"]) 
        if not role in ctx.author.roles: 
            return 

        await ctx.message.delete() 
        embed = discord.Embed(color = 0xFB9E14) 
        embed.set_footer(text = f'Ответ был дан модератором {ctx.author.display_name}', icon_url = self.bot.user.avatar_url) 
        return await ctx.send(f'`[UPDATE!] Ответ на Ваш вопрос был дан. Могу ли я поставить статус "Закрыт" вашему вопросу?`\n`Если у Вас по прежнему остались вопросы, задавайте их прямо здесь.`', embed = embed) 

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild == None:
            return

        if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 0:
            return 

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})

        if ctx.channel.id == rep["rchannel"]:
            creport = discord.utils.get(ctx.guild.categories, id = rep["category_id_one"])

            msg = ctx.content.lower()
            if ctx.author.bot:
                if ctx.author.id == 729309765431328799:
                    return
                else:
                    return await ctx.delete()
            else:
                if list(msg)[0] == '!':
                    await ctx.delete()
                    return await ctx.channel.send(embed = setembed(f'✖ Нельзя использовать команды в этом канале!', self.bot.user.avatar_url), delete_after = 5)
                await ctx.delete()

                fx = 0
                if not reports.count_documents({"guild_id": ctx.guild.id, "proverka": 0, "user_id": ctx.author.id}) == 0:
                    if not discord.utils.get(ctx.guild.channels, id = reports.find_one({"guild_id": ctx.guild.id, "proverka": 0, "user_id": ctx.author.id})["rep_chat"]) == None:
                        return await ctx.channel.send(f'`[ERROR]` {ctx.author.mention}, `Вы уже имеете активный репорт! Для перехода в него нажмите на его название -` <#{reports.find_one({"guild_id": ctx.guild.id, "proverka": 0, "user_id": ctx.author.id})["rep_chat"]}>.', delete_after=10)
                    else:
                        reports.delete_one({"guild_id": ctx.guild.id, "proverka": 0, "user_id": ctx.author.id})
                        fx = 1

                channel = await ctx.guild.create_text_channel(f'Вопрос {rep["number"]}', overwrites=None, category=creport, reason='Создание нового Вопроса.')
                number = rep["number"]
                reports.update_one({"guild_id": ctx.guild.id, "proverka": 1}, {"$set": {"number": rep["number"] + 1}})
                await ctx.channel.send(embed=discord.Embed(description = f'**{ctx.author.mention}, Для вас создан канал - <#{channel.id}>, там Вы получите техническую поддержку от наших модераторов!**', colour=0xFB9E14), delete_after=20)
                await channel.set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True)
                embed1 = discord.Embed(description=f'''**Обращение к поддержке Discord**''', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
                embed1.add_field(name='`Отправитель`\n', value=f'**{ctx.author}**', inline=False)
                embed1.add_field(name='`Суть обращения`', value=f'**{ctx.content}**', inline=False)
                if rep["footer"] == "None":
                    embed1.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                else:
                    embed1.set_footer(text = f'{rep["footer"]}', icon_url = self.bot.user.avatar_url)
                await channel.send(f'{ctx.author.mention} для команды поддержки <@&{rep["support_role"]}>\n', embed=embed1)
                if not rep["himes"] == "None":
                    await channel.send(embed = setembed(f'`[HIMES]:` {ctx.author.mention}, `{rep["himes"]}`', self.bot.user.avatar_url), delete_after = 30)
                if fx == 0:
                    x = int(rep["vsego"]) + 1
                    y = int(rep["active"]) + 1
                    reports.update_one({"proverka": 1, "guild_id": ctx.guild.id}, {"$set": {"vsego": x, "active": y, "last_name": ctx.author.display_name}})
                else:
                    x = int(rep["vsego"])
                    y = int(rep["active"])
                txt = ctx.content.replace('"', '')
                message_id = rep["message_id"]
                chans = self.bot.get_channel(rep["channel"])
                message = await chans.fetch_message(message_id)
                emb23 = discord.Embed(description = f'Доброго времени суток! Вы попали в канал технической поддержки сервера **{ctx.guild.name}**\nТут Вы можете узнать, как получить техническую поддержку от наших модераторов <@&{rep["support_role"]}>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
                emb23.set_author(name=f'{ctx.guild.name} | Support', icon_url= 'https://mydovidka.com/wp-content/uploads/2019/11/de0e202e9992854eade6f1ddf73dff49.png')
                emb23.add_field(name = 'Правила создания репорта', value = '```> Запрещены сообщения не несущие информации или вопроса.\n> Запрещено использовать ненормативную лексику.\n> Запрещено флудить @упоминаниями.\n> Запрещено создавать репорт с некорректным вопросом.\n> Запрещено оскорбительное и неадекватное поведение.\n> Для того что бы задать вопрос, вам необходимо написать его в этот канал.```', inline = False)
                emb23.add_field(name = 'Общее количество', value='\n'f'**⚙** `{x}` вопросов', inline = True)
                emb23.add_field(name = 'На рассмотрении', value = f'**⚙** `{y}` вопросов', inline = True)
                emb23.add_field(name = 'Обработано', value = f'**⚙** `{rep["close"]}` вопросов\n', inline=True)
                emb23.add_field(name = 'Последний вопрос от:', value=f'`{ctx.author.display_name}`', inline = False)
                if rep["image"] == "None":
                    emb23.set_image(url= 'https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif')
                else:
                    emb23.set_image(url= rep["image"])
                emb23.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                emb23.set_thumbnail(url= ctx.guild.icon_url)
                await message.edit(embed=emb23)
                logchan = self.bot.get_channel(rep["logchan"])
                if rep["donate"] == 1:
                    if reports.find_one({"guild_id": ctx.guild.id, "proverka": 3})["sender"] == 0:
                        await logchan.send(f'<@&{rep["support_role"]}>', embed=discord.Embed(description=f'**Поступила новая жалоба от пользователя {ctx.author}.\nОна находится в канале `#{channel.name}`\n\nВам доступны команды:\n`>` {rep["prefix"]}hi - Поздороваться с человеком написавшим репорт\n`>` {rep["prefix"]}by - Задать вопрос: "Можно ли закрывать репорт"\n\n`>` {rep["prefix"]}close `- Закрыть жалобу`\n`>` {rep["prefix"]}active `- Поставить жалобу на рассмотрение.`\n`>` {rep["prefix"]}add @Пользователь#1234 `- Добавить пользователя к вопросу`**', colour=0xFB9E14))
                        reports.insert_one({"guild_id": ctx.guild.id, "proverka": 0, "number": number, "user_id": ctx.author.id, "rep_chat": channel.id, "numid": ctx.author.id, "text": txt, "sendcheck": 0})
                    else:
                        adre = await logchan.send(f'<@&{rep["support_role"]}>', embed=discord.Embed(description=f'**Поступила новая жалоба от пользователя {ctx.author}.\nОна находится в канале `#{channel.name}`\n\nВам доступны команды:\n`>` {rep["prefix"]}hi - Поздороваться с человеком написавшим репорт\n`>` {rep["prefix"]}by - Задать вопрос: "Можно ли закрывать репорт"\n\n`>` {rep["prefix"]}close `- Закрыть жалобу`\n`>` {rep["prefix"]}active `- Поставить жалобу на рассмотрение.`\n`>` {rep["prefix"]}add @Пользователь#1234 `- Добавить пользователя к вопросу`\n\nДля того, что бы взять этот вопрос нажмите на 💌 под этим сообщением!**', colour=0xFB9E14))
                        reports.insert_one({"guild_id": ctx.guild.id, "proverka": 0, "number": number, "user_id": ctx.author.id, "moder": 0, "rep_chat": channel.id, "rep_id": adre.id, "numid": ctx.author.id, "text": txt, "sendcheck": 1})
                        await adre.add_reaction('💌')
                else:
                    await logchan.send(f'<@&{rep["support_role"]}>', embed=discord.Embed(description=f'**Поступила новая жалоба от пользователя {ctx.author}.\nОна находится в канале `#{channel.name}`\n\nВам доступны команды:\n`>` {rep["prefix"]}hi - Поздороваться с человеком написавшим репорт\n`>` {rep["prefix"]}by - Задать вопрос: "Можно ли закрывать репорт"\n\n`>` {rep["prefix"]}close `- Закрыть жалобу`\n`>` {rep["prefix"]}active `- Поставить жалобу на рассмотрение.`\n`>` {rep["prefix"]}add @Пользователь#1234 `- Добавить пользователя к вопросу`**', colour=0xFB9E14))
                    reports.insert_one({"guild_id": ctx.guild.id, "proverka": 0, "number": number, "user_id": ctx.author.id, "rep_chat": channel.id, "numid": ctx.author.id, "text": txt, "sendcheck": 0})

        else:
            info = reports.find_one({"proverka": 2})
            if ctx.content == f'<@!{self.bot.user.id}>' or ctx.content == f'<@{self.bot.user.id}>':
                prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
                await ctx.channel.send(f'{ctx.author.mention},', embed = discord.Embed(title = 'Основная информация', description = f'**> `Мой создатель:` [{info["discord"]}]({info["vk"]})\n> `Сервер технической поддержки:` {info["server"]}\n> `Префикс установленный на этом сервере:`   {prefix}\n> `Ссылка на добавление бота:` https://discord.com/api/oauth2/authorize?client_id=729309765431328799&permissions=8&scope=bot\n> `Узнать команды бота:` {prefix}help**\n> - `Для создания вопроса, необходимо написать его в канал` <#{rep["rchannel"]}>\n\n💰 **Приобретение дополнительных функций возможно только у разработчика([{info["discord"]}]({info["vk"]}))**', colour = 0xFB9E14), delete_after = 60)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global register
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
            return

        if reports.count_documents({"guild_id": payload.guild_id, "proverka": 1}) == 0:
            return 

        rep = reports.find_one({"guild_id": payload.guild_id, "proverka": 1})

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            return
        channel = self.bot.get_channel(payload.channel_id)
        emoji = str(payload.emoji)
        memb = payload.member
        if emoji == '▶':
            if payload.guild_id in register:
                return
            if channel.id == rep["start_channel"]:
                register.append(payload.guild_id)
                embed = discord.Embed(description = f'Что бы начать работать со мной, мне необходимо узнать некоторые данные:\n> `Какой канал для написания вопросов`\n> `Какие категории будут хранить вопросы, корзину и список активных вопросов`\n> `Какая роль у технической поддержки этого сервера`\n> `Какой канал логирования у этого сервера`\n\n**Укажите все данные вручную, нажав на ✔**\n**Или используйте автоматическое заполнение, нажав на ⏩**', colour=0xFB9E14)
                embed.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                imes = await channel.send(embed = embed)
                await imes.add_reaction('✔')
                await imes.add_reaction('⏩')
                try:
                    react, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda react, user: user == memb and react.message.channel == channel and react.emoji in ['✔', '⏩'])
                except Exception:
                    try:
                        register.remove(payload.guild_id)
                    except:
                        pass
                    return await imes.delete()
                else:
                    if str(react.emoji) == '⏩':
                        one, two, three, four, five, six = 1703, 1703, 1703, 1703, 1703,  1703
                        text1, text2, text3, text4, text5, text6 = 'Будет создан автоматически', 'Будет создана автоматически', 'Будет создана автоматически', 'Будет создана автоматически', 'Будет создана автоматически', 'Будет создан автоматически'
                        zap = await channel.send(embed = setembed(f'**Происходит процесс регистрации сервера в базе данных.**\n\n> `1.` Канал написания вопросов: {text1}\n> `2.` Категория с активными вопросами: {text2}.\n> `3.` Категория с вопросами на рассмотрении: {text3}.\n> `4.` Категория с закрытыми вопросами(Корзина): {text4}.\n> `5.` Роль технической поддержки сервера: {text5}\n> `6.` Канал логирования всех репортов: {text6}\n\n', self.bot.user.avatar_url))

                    elif str(react.emoji) == '✔':
                        zap = await channel.send(embed = setembed(f'Отлично, теперь мы можем начать настройку!\nНиже, будет прописан ход заполнения необходимой мне информации, а последняя строка скажет Вам, что необходимо ввести.\n\n> `1.` Канал написания вопросов: Не заполнено\n> `2.` Категория с активными вопросами: Не заполнено.\n> `3.` Категория с вопросами на рассмотрении: Не заполнено.\n> `4.` Категория с закрытыми вопросами: Не заполнено.\n> `5.` Роль технической поддержки сервера: Не заполнено.\n> `6.` Канал логирования всех репортов: Не заполнено.\n\n**Укажите канал для написания вопросов(Можно использовать ID) | Для автоматического создания введите: +**\n**Для отмены действия, введите:** `Отмена`', self.bot.user.avatar_url))
                        def check(m):
                            return m.author.id == memb.id and m.channel.id == channel.id
                        try:
                            msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                        except Exception:
                            
                            await imes.delete()
                            try:
                                register.remove(payload.guild_id)
                            except:
                                pass
                            return await zap.delete()
                        else:
                            if msg.content.lower() == 'отмена':
                                
                                await channel.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                try:
                                    await msg.delete()
                                except:
                                    pass
                                await imes.delete()
                                try:
                                    register.remove(payload.guild_id)
                                except:
                                    pass
                                return await zap.delete()
                            if msg.content.lower() == '+':
                                one, text1 = 1703, 'Будет создан автоматически'
                            else:
                                if "<#" in msg.content.split()[0]:
                                    one = msg.content.split()[0].split('#')[1].replace('>', '')
                                    text1 = f'<#{one}>'
                                else:
                                    one = msg.content.split()[0]
                                    text1 = f'<#{one}>'
                                try:
                                    one = int(one)
                                except:
                                    
                                    await channel.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                                if not int(one) in [i.id for i in guild.text_channels]:
                                    
                                    await channel.send(embed = setembed('✖ Такого канала не существует в данном дискорде!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                            try:
                                await msg.delete()
                            except:
                                pass
                            await channel.send(embed = setembed('✔ Вы успешно выполнили действие: Указать канал вопросов.\nВыполните новое действие: Указать ID категории с активными вопросами.', self.bot.user.avatar_url), delete_after = 5)
                        await zap.edit(embed = setembed(f'Отлично, теперь мы можем начать настройку!\nНиже, будет прописан ход заполнения необходимой мне информации, а последняя строка скажет Вам, что необходимо ввести.\n\n> `1.` Канал написания вопросов: {text1}\n> `2.` Категория с активными вопросами: Не заполнено.\n> `3.` Категория с вопросами на рассмотрении: Не заполнено.\n> `4.` Категория с закрытыми вопросами: Не заполнено.\n> `5.` Роль технической поддержки сервера: Не заполнено.\n> `6.` Канал логирования всех репортов: Не заполнено.\n\n**Укажите ID категории с активными вопросами | Для автоматического создания введите: +**', self.bot.user.avatar_url))
                        def check(m):
                            return m.author.id == memb.id and m.channel.id == channel.id
                        try:
                            msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                        except Exception:
                            await zap.delete()
                            try:
                                register.remove(payload.guild_id)
                            except:
                                pass
                            return await imes.delete()
                        else:
                            if msg.content.lower() == 'отмена':
                                await channel.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                try:
                                    await msg.delete()
                                except:
                                    pass
                                await imes.delete()
                                
                                try:
                                    register.remove(payload.guild_id)
                                except:
                                    pass
                                return await zap.delete()
                            if msg.content.lower() == '+':
                                two, text2 = 1703, 'Будет создана автоматически'
                            else:
                                try:
                                    two = int(msg.content.split()[0])
                                    text2 = f'{discord.utils.get(guild.categories, id = two).name}'
                                except:
                                    await channel.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                                if not int(two) in [i.id for i in guild.categories]:
                                    await channel.send(embed = setembed('✖ Такой категории не существует в данном дискорде. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 10)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                            try:
                                await msg.delete()
                            except:
                                pass
                            await channel.send(embed = setembed('✔ Вы успешно выполнили действие: Указать категорию с вопросами.\nВыполните новое действие: Указать ID категории с вопросами на рассмотрении.', self.bot.user.avatar_url), delete_after = 5)
                        await zap.edit(embed = setembed(f'Отлично, теперь мы можем начать настройку!\nНиже, будет прописан ход заполнения необходимой мне информации, а последняя строка скажет Вам, что необходимо ввести.\n\n> `1.` Канал написания вопросов: {text1}\n> `2.` Категория с активными вопросами: {text2}.\n> `3.` Категория с вопросами на рассмотрении: Не заполнено.\n> `4.` Категория с закрытыми вопросами: Не заполнено.\n> `5.` Роль технической поддержки сервера: Не заполнено.\n> `6.` Канал логирования всех репортов: Не заполнено.\n\n**Укажите ID категории с вопросами на рассмотрении | Для автоматического создания введите: +**', self.bot.user.avatar_url))
                        def check(m):
                            return m.author.id == memb.id and m.channel.id == channel.id
                        try:
                            msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                        except Exception:
                            await zap.delete()
                            try:
                                register.remove(payload.guild_id)
                            except:
                                pass
                            return await imes.delete()
                        else:
                            if msg.content.lower() == 'отмена':
                                await channel.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                try:
                                    await msg.delete()
                                except:
                                    pass
                                await imes.delete()
                                
                                try:
                                    register.remove(payload.guild_id)
                                except:
                                    pass
                                return await zap.delete()
                            if msg.content.lower() == '+':
                                three, text3 = 1703, 'Будет создана автоматически'
                            else:
                                try:
                                    three = int(msg.content.split()[0])
                                    text3 = f'{discord.utils.get(guild.categories, id = three).name}'
                                except:
                                    await channel.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                                if not int(three) in [i.id for i in guild.categories]:
                                    await channel.send(embed = setembed('✖ Такой категории не существует в данном дискорде. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 10)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                            try:
                                await msg.delete()
                            except:
                                pass
                            await channel.send(embed = setembed('✔ Вы успешно выполнили действие: Указать категорию с вопросами на рассмотрении.\nВыполните новое действие: Указать ID категории с закрытыми вопросами(Корзина)', self.bot.user.avatar_url), delete_after = 5)
                        await zap.edit(embed = setembed(f'Отлично, теперь мы можем начать настройку!\nНиже, будет прописан ход заполнения необходимой мне информации, а последняя строка скажет Вам, что необходимо ввести.\n\n> `1.` Канал написания вопросов: {text1}\n> `2.` Категория с активными вопросами: {text2}.\n> `3.` Категория с вопросами на рассмотрении: {text3}.\n> `4.` Категория с закрытыми вопросами(Корзина): Не заполнено.\n> `5.` Роль технической поддержки сервера: Не заполнено.\n> `6.` Канал логирования всех репортов: Не заполнено.\n\n**Укажите ID категории с закрытыми вопросами(Корзина) | Для автоматического создания введите: +**', self.bot.user.avatar_url))
                        def check(m):
                            return m.author.id == memb.id and m.channel.id == channel.id
                        try:
                            msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                        except Exception:
                            await zap.delete()
                            try:
                                register.remove(payload.guild_id)
                            except:
                                pass
                            return await imes.delete()
                        else:
                            if msg.content.lower() == 'отмена':
                                await channel.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                try:
                                    await msg.delete()
                                except:
                                    pass
                                await imes.delete()
                                try:
                                    register.remove(payload.guild_id)
                                except:
                                    pass
                                return await zap.delete()
                            if msg.content.lower() == '+':
                                four, text4 = 1703, 'Будет создана автоматически'
                            else:
                                try:
                                    four = int(msg.content.split()[0])
                                    text4 = f'{discord.utils.get(guild.categories, id = four).name}'
                                except:
                                    await channel.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                                if not int(four) in [i.id for i in guild.categories]:
                                    await channel.send(embed = setembed('✖ Такой категории не существует в данном дискорде. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 10)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                            try:
                                await msg.delete()
                            except:
                                pass
                            await channel.send(embed = setembed('✔ Вы успешно выполнили действие: Указать категорию с закрытыми вопросами(Корзина).\nВыполните новое действие: Указать роль технической поддержки сервера.', self.bot.user.avatar_url), delete_after = 5)
                        await zap.edit(embed = setembed(f'Отлично, теперь мы можем начать настройку!\nНиже, будет прописан ход заполнения необходимой мне информации, а последняя строка скажет Вам, что необходимо ввести.\n\n> `1.` Канал написания вопросов: {text1}\n> `2.` Категория с активными вопросами: {text2}.\n> `3.` Категория с вопросами на рассмотрении: {text3}.\n> `4.` Категория с закрытыми вопросами(Корзина): {text4}.\n> `5.` Роль технической поддержки сервера: Не заполнено.\n> `6.` Канал логирования всех репортов: Не заполнено.\n\n**Укажите роль технической поддержки сервера | Для автоматического создания введите: +**', self.bot.user.avatar_url))
                        def check(m):
                            return m.author.id == memb.id and m.channel.id == channel.id
                        try:
                            msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                        except Exception:
                            await imes.delete()
                            try:
                                register.remove(payload.guild_id)
                            except:
                                pass
                            return await zap.delete()
                        else:
                            if msg.content.lower() == 'отмена':
                                await channel.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 3)
                                try:
                                    await msg.delete()
                                except:
                                    pass
                                await imes.delete()
                                try:
                                    register.remove(payload.guild_id)
                                except:
                                    pass
                                return await zap.delete()
                            if msg.content.lower() == '+':
                                five, text5 = 1703, 'Будет создана автоматически'
                            else:
                                if "<@&" in msg.content.split()[0]:
                                    five = msg.content.split()[0].split('&')[1].replace('>', '')
                                    text5 = f'<@&{five}>'
                                else:
                                    five = msg.content.split()[0]
                                    text5 = f'<@&{five}>'
                                try:
                                    five = int(five)
                                except:
                                    await channel.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                                if not int(five) in [i.id for i in guild.roles]:
                                    await channel.send(embed = setembed('✖ Такой роли не существует в данном дискорде!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                            try:
                                await msg.delete()
                            except:
                                pass
                            await channel.send(embed = setembed('✔ Вы успешно выполнили действие: Указать роль технической поддержки.\nВыполните новое действие: Указать канал с логированием всех репортов', self.bot.user.avatar_url), delete_after = 5)
                        await zap.edit(embed = setembed(f'Отлично, теперь мы можем начать настройку!\nНиже, будет прописан ход заполнения необходимой мне информации, а последняя строка скажет Вам, что необходимо ввести.\n\n> `1.` Канал написания вопросов: {text1}\n> `2.` Категория с активными вопросами: {text2}.\n> `3.` Категория с вопросами на рассмотрении: {text3}.\n> `4.` Категория с закрытыми вопросами(Корзина): {text4}.\n> `5.` Роль технической поддержки сервера: {text5}\n> `6.` Канал логирования всех репортов: Не заполнено.\n\n**Укажите канал с логированием всех репортов | Для автоматического создания введите: +**', self.bot.user.avatar_url))
                        def check(m):
                            return m.author.id == memb.id and m.channel.id == channel.id
                        try:
                            msg = await self.bot.wait_for('message', timeout= 120.0, check = check)
                        except Exception:
                            await imes.delete()
                            try:
                                register.remove(payload.guild_id)
                            except:
                                pass
                            return await zap.delete()
                        else:
                            if msg.content.lower() == 'отмена':
                                await channel.send(embed = setembed('✔ Вы успешно отменили действие!', self.bot.user.avatar_url), delete_after = 5)
                                try:
                                    await msg.delete()
                                except:
                                    pass
                                await imes.delete()
                                try:
                                    register.remove(payload.guild_id)
                                except:
                                    pass
                                return await zap.delete()
                            if msg.content.lower() == '+':
                                six, text6 = 1703, 'Будет создан автоматически'
                            else:
                                if "<#" in msg.content.split()[0]:
                                    six = msg.content.split()[0].split('#')[1].replace('>', '')
                                    text6 = f'<#{six}>'
                                else:
                                    six = msg.content.split()[0]
                                    text6 = f'<#{six}>'
                                try:
                                    six = int(six)
                                except:
                                    await channel.send(embed = setembed('✖ Данные указаны не верно. Начните заполнение сначала!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                                if not int(six) in [i.id for i in guild.text_channels]:
                                    await channel.send(embed = setembed('✖ Такого канала не существует в данном дискорде!', self.bot.user.avatar_url), delete_after = 5)
                                    try:
                                        await msg.delete()
                                    except:
                                        pass
                                    await imes.delete()
                                    try:
                                        register.remove(payload.guild_id)
                                    except:
                                        pass
                                    return await zap.delete()
                        try:
                            await msg.delete()
                        except:
                            pass
                        await zap.edit(embed = setembed(f'**Происходит процесс регистрации сервера в базе данных.**\n\n> `1.` Канал написания вопросов: {text1}\n> `2.` Категория с активными вопросами: {text2}.\n> `3.` Категория с вопросами на рассмотрении: {text3}.\n> `4.` Категория с закрытыми вопросами(Корзина): {text4}.\n> `5.` Роль технической поддержки сервера: {text5}\n> `6.` Канал логирования всех репортов: {text6}\n\n', self.bot.user.avatar_url))

                    
                    if five == 1703:
                        newrole = await guild.create_role(name = '★ Support Team ★', colour = discord.Colour(0x10d30d)) 
                        five = newrole.id

                    emb23 = discord.Embed(description = f'Доброго времени суток! Вы попали в канал технической поддержки сервера **{guild.name}**.\nТут Вы можете узнать, как получить техническую поддержку от наших модераторов <@&{five}>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
                    emb23.set_author(name=f'{guild.name} | Support', icon_url='https://mydovidka.com/wp-content/uploads/2019/11/de0e202e9992854eade6f1ddf73dff49.png')
                    emb23.add_field(name = 'Правила создания репорта', value = '```> Запрещены сообщения не несущие информации или вопроса.\n> Запрещено использовать ненормативную лексику.\n> Запрещено флудить @упоминаниями.\n> Запрещено создавать репорт с некорректным вопросом.\n> Запрещено оскорбительное и неадекватное поведение.\n> Для того что бы задать вопрос, вам необходимо написать его в этот канал.```', inline = False)
                    emb23.add_field(name=f'Общее количество', value=f'**⚙** `0` вопросов', inline = True)
                    emb23.add_field(name = 'На рассмотрении', value = f'**⚙** `0` вопросов', inline = True)
                    emb23.add_field(name = 'Обработано', value = f'**⚙** `0` вопросов\n', inline=True)
                    emb23.set_thumbnail(url=guild.icon_url)
                    emb23.add_field(name = 'Последний вопрос от:', value=f'`-`', inline = False)
                    emb23.set_image(url= 'https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif')
                    emb23.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                    if one == 1703:
                        newchannel = await guild.create_text_channel(f'❓┃поддержка', overwrites=None, reason='Создание канала для написани вопросов')
                        one = newchannel.id
                        mesad = await newchannel.send(embed = emb23)
                    else:
                        await self.bot.get_channel(one).purge(limit = 1000)
                        mesad = await self.bot.get_channel(one).send(embed = emb23)
                    
                    await zap.edit(embed = setembed(f'**Происходит процесс регистрации сервера в базе данных.**\n\n> `1.` Канал написания вопросов: {text1} | ✔\n> `2.` Категория с активными вопросами: {text2}\n> `3.` Категория с вопросами на рассмотрении: {text3}\n> `4.` Категория с закрытыми вопросами(Корзина): {text4}\n> `5.` Роль технической поддержки сервера: {text5} | ✔\n> `6.` Канал логирования всех репортов: {text6}\n\n', self.bot.user.avatar_url))

                    if two == 1703:
                        newcat1 = await guild.create_category(name = 'Активные вопросы', reason='Создание катигории для активных вопросов')
                        await newcat1.set_permissions(discord.utils.get(guild.roles, id = five), read_messages = True, send_messages = True, read_message_history = True)
                        await newcat1.set_permissions(guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                        two = newcat1.id
                    else:
                        await discord.utils.get(guild.categories, id = two).set_permissions(discord.utils.get(guild.roles, id = five), read_messages = True, send_messages = True, read_message_history = True)
                        await discord.utils.get(guild.categories, id = two).set_permissions(guild.default_role, read_messages = True, send_messages = True, read_message_history = True)

                    if three == 1703:
                        newcat2 = await guild.create_category(name = 'На рассмотрении', reason='Создание категории для вопросов стоящих на рассмотрении')
                        await newcat2.set_permissions(discord.utils.get(guild.roles, id = five), read_messages = True, send_messages = True, read_message_history = True)
                        await newcat2.set_permissions(guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                        three = newcat2.id
                    else:
                        await discord.utils.get(guild.categories, id = three).set_permissions(discord.utils.get(guild.roles, id = five), read_messages = True, send_messages = True, read_message_history = True)
                        await discord.utils.get(guild.categories, id = three).set_permissions(guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                    if four == 1703:
                        newcat3 = await guild.create_category(name = 'Корзина', reason='Создание корзины')
                        await newcat3.set_permissions(discord.utils.get(guild.roles, id = five), read_messages = True, send_messages = False, read_message_history = True)
                        await newcat3.set_permissions(guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                        four = newcat3.id
                    else:
                        await discord.utils.get(guild.categories, id = four).set_permissions(discord.utils.get(guild.roles, id = five), read_messages = True, send_messages = False, read_message_history = True)
                        await discord.utils.get(guild.categories, id = four).set_permissions(guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                    await zap.edit(embed = setembed(f'**Происходит процесс регистрации сервера в базе данных.**\n\n> `1.` Канал написания вопросов: {text1} | ✔\n> `2.` Категория с активными вопросами: {text2} | ✔\n> `3.` Категория с вопросами на рассмотрении: {text3} | ✔\n> `4.` Категория с закрытыми вопросами(Корзина): {text4} | ✔\n> `5.` Роль технической поддержки сервера: {text5} | ✔\n> `6.` Канал логирования всех репортов: {text6}\n\n', self.bot.user.avatar_url))

                    if six == 1703:
                        newchannel2 = await guild.create_text_channel(f'❕┃логи-репорта', overwrites=None, reason='Создание канала для логирования репорта.')
                        await newchannel2.set_permissions(discord.utils.get(guild.roles, id = five), read_messages = True, send_messages = False, read_message_history = True)
                        await newchannel2.set_permissions(guild.default_role, read_messages = False, send_messages = False, read_message_history = False)
                        six = newchannel2.id
                    else:
                        await self.bot.get_channel(six).set_permissions(discord.utils.get(guild.roles, id = five), read_messages = True, send_messages = False, read_message_history = True)
                        await self.bot.get_channel(six).set_permissions(guild.default_role, read_messages = False, send_messages = False, read_message_history = False)

                    reports.update_one({"guild_id": guild.id, "proverka": 1}, {"$set": {"rchannel": one, "category_id_one": two, "category_id_two": three, "category_id_three": four, "number": 1, "channel": one, "message_id": mesad.id, "logchan": six, "support_role": five, "start_channel": 0}})

                    await zap.edit(embed = setembed(f'**Настройка бота успешно закончена!\n**\n\n> `1.` Канал написания вопросов: {text1} | ✔\n> `2.` Категория с активными вопросами: {text2} | ✔\n> `3.` Категория с вопросами на рассмотрении: {text3} | ✔\n> `4.` Категория с закрытыми вопросами(Корзина): {text4} | ✔\n> `5.` Роль технической поддержки сервера: {text5} | ✔\n> `6.` Канал логирования всех репортов: {text6} | ✔\n\n**Дополнительную информацию Вы можете получить просто упомянув бота в чате!\nПриятного использования ❤**', self.bot.user.avatar_url))
                    await asyncio.sleep(30)
                    await channel.delete()
                    register.remove(payload.guild_id)
                                       
        if channel.id != rep["logchan"]:
            return
        message = await channel.fetch_message(payload.message_id)
        if not discord.utils.get(message.guild.roles, id = rep["support_role"]) in memb.roles:
            return
        
        if rep["donate"] == 0:
            return

        if reports.find_one({"guild_id": payload.guild_id, "proverka": 3})["sender"] == 0:
            return

        if emoji == '💌':

            if reports.count_documents({"rep_id": message.id}) == 0:
              await message.delete()
              return await channel.send(f'`[BUGTRACKER]:` `Был удалён багнутый репорт. ID: {message.id}`')

            if reports.find_one({"rep_id": message.id})["moder"] > 0:
              mem = discord.utils.get(guild.members, id= reports.find_one({"rep_id": message.id})["moder"])
              return await channel.send(f'`[NO ACCEPT]:` `Данный репорт был принят другим модератором({mem.display_name})`',delete_after=5)

            if reports.count_documents({"moder": memb.id}) == 1:
                return await channel.send(f'`[NO ACCEPT]:` `Для начала закройте свой репорт(`<#{reports.find_one({"moder": memb.id})["rep_chat"]}>`), что бы приняться за этот.`',delete_after=5)
            
            chat = guild.get_channel(reports.find_one({"rep_id": message.id})["rep_chat"])
            prvvop = re.findall(r'\w*', chat.name)
            if reports.find_one({"guild_id": guild.id, "proverka": 0, "number": int(prvvop[2])})["user_id"]  == memb.id:
                return await channel.send(embed = setembed(f'{memb.display_name}, модераторам запрещено принимать собственный репорт.\n`[P.S]: Это сделано в целях защиты от накрутки статистики.`', self.bot.user.avatar_url), delete_after = 7)

            reports.update_one({"rep_id": message.id}, {"$set": {"moder": memb.id}})
            await chat.set_permissions(memb,read_messages=True,read_message_history=True,send_messages=True)
            prvvop = re.findall(r'\w*', chat.name)
            await chat.send(f'`[NOTIFICATION]` `Агент технической поддержки` {memb.mention} `принял ваш репорт.`')
            member = discord.utils.get(guild.members, id=reports.find_one({"guild_id": guild.id, "proverka": 0, "number": int(prvvop[2])})["user_id"]) 
            await message.edit(content=f'<@&{rep["support_role"]}>', embed=discord.Embed(description=f'**Поступила новая жалоба от пользователя {member}.\nОна находится в канале `#{chat.name}`\n\nВам доступны команды:\n`>` {rep["prefix"]}hi - Поздороваться с человеком написавшим репорт\n`>` {rep["prefix"]}by - Задать вопрос: "Можно ли закрывать репорт"\n\n`>` {rep["prefix"]}close `- Закрыть жалобу`\n`>` {rep["prefix"]}active `- Поставить жалобу на рассмотрение.`\n`>` {rep["prefix"]}add @Пользователь#1234 `- Добавить пользователя к вопросу`\n\nМодератор {memb.display_name} принялся за данный репорт.**', colour=0xFB9E14))
            add(guild.id, memb, "addme")
            await message.clear_reactions()

    @commands.command(aliases=['close'])
    async def close_report(self, ctx):
        if ctx.guild == None:
            return

        if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 0:
            return 

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})

        await ctx.message.delete()
        prvvop = re.findall(r'\w*', ctx.channel.name)
        if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 0, "rep_chat": ctx.channel.id}) == 0:
            return

        try:
            member = discord.utils.get(ctx.guild.members, id=reports.find_one({"guild_id": ctx.guild.id, "proverka": 0, "rep_chat": ctx.channel.id})["user_id"]) 
        except:
            return

        if not discord.utils.get(ctx.guild.roles, id=rep["support_role"]) in ctx.author.roles:
            return

        if rep["donate"] == 1:
            if reports.find_one({"guild_id": ctx.guild.id, "rep_chat": ctx.channel.id})["sendcheck"] == 1:
                if not ctx.author.id == reports.find_one({"guild_id": ctx.guild.id, "rep_chat": ctx.channel.id})["moder"]:
                    return

        if reports.count_documents({"guild_id": ctx.guild.id, "rep_chat": ctx.channel.id}) > 0:
          nmb = reports.find_one({"guild_id": ctx.guild.id, "rep_chat": ctx.channel.id})["number"]
          z = int(rep["close"]) + 1
          y = int(rep["active"]) - 1
          try:
            reports.update_one({"proverka": 1, "guild_id": ctx.guild.id}, {"$set": {"close": z, "active": y, "last_name": member.display_name}})
          except:
            member = ctx.author
            reports.update_one({"proverka": 1, "guild_id": ctx.guild.id}, {"$set": {"close": z, "active": y, "last_name": ctx.author.display_name}})
          message_id = rep["message_id"]
          chans = self.bot.get_channel(rep["channel"])
          message = await chans.fetch_message(message_id)
          emb23 = discord.Embed(description = f'Доброго времени суток! Вы попали в канал технической поддержки сервера **{ctx.guild.name}**.\nТут Вы можете узнать, как получить техническую поддержку от наших модераторов <@&{rep["support_role"]}>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
          emb23.set_author(name=f'{ctx.guild.name} | Support', icon_url='https://mydovidka.com/wp-content/uploads/2019/11/de0e202e9992854eade6f1ddf73dff49.png')
          emb23.add_field(name = 'Правила создания репорта', value = '```> Запрещены сообщения не несущие информации или вопроса.\n> Запрещено использовать ненормативную лексику.\n> Запрещено флудить @упоминаниями.\n> Запрещено создавать репорт с некорректным вопросом.\n> Запрещено оскорбительное и неадекватное поведение.\n> Для того что бы задать вопрос, вам необходимо написать его в этот канал.```', inline = False)
          emb23.add_field(name=f'Общее количество', value=f'**⚙** `{rep["vsego"]}` вопросов', inline = True)
          emb23.add_field(name = 'На рассмотрении', value = f'**⚙** `{y}` вопросов', inline = True)
          emb23.add_field(name = 'Обработано', value = f'**⚙** `{z}` вопросов\n', inline=True)
          emb23.set_thumbnail(url=ctx.guild.icon_url)
          emb23.add_field(name = 'Последний вопрос от:', value=f'`{member.display_name}`', inline = False)
          if rep["image"] == "None":
            emb23.set_image(url= 'https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif')
          else:
            emb23.set_image(url= rep["image"])
          emb23.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
          await message.edit(embed=emb23)
          rolesupport = discord.utils.get(ctx.guild.roles, id=rep["support_role"])
          await ctx.channel.send(embed=discord.Embed(description=f'`Вопросу` **№{nmb}** `установлен статус "Закрыт".`\n`Источник:` <@!{ctx.author.id}>',colour=0xFB9E14))
          await ctx.channel.set_permissions(member,read_messages=True, send_messages=False, read_message_history=True)
          await ctx.channel.set_permissions(rolesupport, read_messages=True, send_messages=False, read_message_history=True)
          messages = await ctx.channel.history(limit=1000).flatten()
          k = -1

          for i in range(len(messages) // 2):
              messages[k], messages[i] = messages[i], messages[k]
              k -= 1

          obfile = open(f'ticket-{nmb}.txt', 'w', encoding='utf-8')
          obfile.write(f'[System]: Создание вопроса пользователем {member.display_name}({member})\nК сообщению был добавлен вопрос: "{reports.find_one({"rep_chat": ctx.channel.id})["text"]}"\n\n')
          for i in messages:
              try:
                mas = [ ]
                if len(i.content) == 0:
                    v = f'\n-----------------------\nОтправлено Embed-сообщение\nОтправитель: {i.author}\nОтправлено: {i.created_at.strftime("%m, %d - %H:%M:%S")}\nПрочитать его можно в канале "{ctx.channel.name}" до момента его удаления.\n-----------------------\n'
                    mas.append(f'{v} ')
                    st = 1
                else:
                    text = i.content.replace('`', '')
                    for v in text.split(' '):
                        if f'<@!{member.id}>' in v:
                            v = v.replace(f'<@!{member.id}>', f'{member.display_name}({member})')                           
                            mas.append(f'{v} ')

                        elif '<@&' in v:
                            v = v.replace('<@&', '').replace('>', '').replace(',', '').replace('.', '').replace(':', '').replace('?', '').replace('!', '')
                            try:   
                                rm = discord.utils.get(ctx.guild.roles, id = int(v))
                                v = f'{rm.name}(Роль)'  
                            except:
                                v = f'"Роль с ID: {v}"'
                            mas.append(f'{v} ')

                        elif '<#' in v:
                            v = v.replace('<#', '').replace('>', '').replace(',', '').replace('.', '').replace(':', '').replace('?', '').replace('!', '')
                            try:   
                                rc = self.bot.get_channel(int(v))
                                v = f'#{rc.name}(Текстовый канал)'  
                            except:
                                v = f'"Текстовый канал с ID: {v}"'
                            mas.append(f'{v} ')

                        elif '<@' in v:
                            v = v.replace('<@', '').replace('>', '').replace(',', '').replace('.', '').replace(':', '').replace('?', '').replace('!', '')
                            try:
                                mem = discord.utils.get(ctx.guild.members, id = int(v))
                                v = f'{mem.display_name}({mem})'
                            except:
                                v = f'"Пользователь с ID: {v}"'
                            mas.append(f'{v} ')
                        else:
                            mas.append(f'{v} ')

                        st = 0
                str_a = ''.join(mas)
                if st == 1:
                    obfile.write(f'{str_a}\n')
                else:
                    obfile.write(f'[{i.created_at.strftime("%m, %d - %H:%M:%S")}]{i.author.display_name}: {str_a}\n\n')
              except:
                  pass
          obfile.write(f'[System]: Закрытие вопроса пользователем {ctx.author.display_name}({ctx.author})')
          obfile.close()

          channel2 = self.bot.get_channel(rep["logchan"])
          await channel2.send(
          embed=discord.Embed(description=f'`Вопросу` **№{nmb}** `установлен статус "Закрыт".`\n`Источник:` <@!{ctx.author.id}>\n\n`Сообщения сохранены в системном файле`',colour=0xFB9E14),file=discord.File(fp=f'ticket-{nmb}.txt'))
          reports.delete_one({"proverka": 0, "rep_chat": ctx.channel.id})
          try:
            await member.send(embed=discord.Embed(description=f'{member.mention}, `вашему вопросу` **№{nmb}** `установлен статус "Закрыт".`\n`Источник:` <@!{ctx.author.id}>\n\n`Сообщения сохранены в системном файле`',colour=0xFB9E14),file=discord.File(fp=f'ticket-{nmb}.txt'))
          except discord.Forbidden:
            pass
          os.remove(f'ticket-{nmb}.txt')
          await ctx.channel.edit(name=f'ticket-{nmb}')
          ccat = discord.utils.get(ctx.guild.categories, id=rep["category_id_three"])
          await ctx.channel.edit(category=ccat)
          add(ctx.guild.id, ctx.author, "close")
          if rep["donate"] == 1:
            if not member == ctx.author or not discord.utils.get(ctx.guild.roles,id=rep["support_role"]) in member.roles:
                if reports.find_one({"guild_id": ctx.guild.id, "proverka": 3})["ocenka"] == 1:
                    mmsg = await ctx.channel.send(f'{member.mention}', embed=discord.Embed(title='Оценка ответа модератора', description=f'**На сколько хорошо ответил модератор {ctx.author.mention}?\nПожалуйста, нажмите на эмодзи с оценкой, на которую Вы оцениваете ответ модератора**'))
                    r_list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']
                    ocv = 0
                    for r in r_list:
                        await mmsg.add_reaction(r)
                    try:
                        react, user = await self.bot.wait_for('reaction_add',timeout=300,check=lambda react, user: user == member and react.message.channel == ctx.channel and react.emoji in r_list)
                    except Exception:
                        await mmsg.delete()
                    else:
                        if str(react.emoji) == r_list[0]:
                            ocv = 1
                            await mmsg.clear_reactions()
                        elif str(react.emoji) == r_list[1]:
                            ocv = 2
                            await mmsg.clear_reactions()
                        elif str(react.emoji) == r_list[2]:
                            ocv = 3
                            await mmsg.clear_reactions()
                        elif str(react.emoji) == r_list[3]:
                            ocv = 4
                            await mmsg.clear_reactions()
                        elif str(react.emoji) == r_list[4]:
                            ocv = 5
                            await mmsg.clear_reactions()
                        if not ocv == 0:
                            await mmsg.edit(context=f'{member.mention}',embed=discord.Embed(title='Оценка ответа модератора',description=f'**Вы оценили ответ модератора {ctx.author.mention} на `{ocv}` баллов**'))
                            await channel2.send(embed=discord.Embed(title='Оценка ответа модератора', description=f'**Пользователь {member} оценил ответ модератора {ctx.author.mention} на `{ocv}` баллов**'))
                            moder.update_one({"guild": ctx.guild.id, "id": ctx.author.id}, {"$set": {"repa": moder.find_one({"id": ctx.author.id})["repa"] + ocv}})
          await asyncio.sleep(600)
          await ctx.channel.delete()
        else:
            return

    @commands.command(aliases=['active'])
    async def fon_active(self, ctx):
        if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 0:
            return 

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})

        await ctx.message.delete()
        prvvop = re.findall(r'\w*', ctx.channel.name)
        if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 0, "rep_chat": ctx.channel.id}) == 0:
            return
        member = discord.utils.get(ctx.guild.members, id=reports.find_one({"guild_id": ctx.guild.id, "proverka": 0, "rep_chat": ctx.channel.id})["user_id"]) 
        if not discord.utils.get(ctx.guild.roles, id=rep["support_role"]) in ctx.author.roles:
            return

        if ctx.channel.category.id == rep["category_id_two"]:
            return

        if rep["donate"] == 1:
            if not ctx.author.id == reports.find_one({"rep_chat": ctx.channel.id})["moder"]:
                return
        nmb = reports.find_one({"guild_id": ctx.guild.id, "rep_chat": ctx.channel.id})["number"]

        await ctx.channel.send(embed=discord.Embed(description=f'{member.mention}, `вашему вопросу` **№{nmb}** `установлен статус "На рассмотрении".`\n`Источник:` <@!{ctx.author.id}>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow()))
        channel2 = self.bot.get_channel(rep["logchan"])
        await channel2.send(embed=discord.Embed(description=f'`Вопросу` **№{nmb}** `установлен статус "На рассмотрении".`\n`Источник:` <@!{ctx.author.id}>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow()))
        ccat = discord.utils.get(ctx.guild.categories, id=rep["category_id_two"])
        await ctx.channel.edit(category=ccat)
        add(ctx.guild.id, ctx.author, "rasm")

    @commands.command(aliases=['add'])
    async def rep_add(self, ctx, member: discord.Member = None):
        if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 0:
            return 

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})

        await ctx.message.delete()

        if member == None or not member in ctx.guild.members:
            return await ctx.send(embed=discord.Embed(description='**:grey_exclamation: Обязательно укажите пользователя!**', color = 0xFB9E14), delete_after=10)
        prvvop = re.findall(r'\w*', ctx.channel.name)
        if reports.count_documents({"guild_id": ctx.guild.id, "proverka": 0, "rep_chat": ctx.channel.id}) == 0:
            return
        memb = discord.utils.get(ctx.guild.members, id=reports.find_one({"guild_id": ctx.guild.id, "proverka": 0, "rep_chat": ctx.channel.id})["user_id"]) 
        if not discord.utils.get(ctx.guild.roles, id=rep["support_role"]) in ctx.author.roles:
            return

        if rep["donate"] == 1:
            if not ctx.author.id == reports.find_one({"rep_chat": ctx.channel.id})["moder"]:
                return
        nmb = reports.find_one({"guild_id": ctx.guild.id, "rep_chat": ctx.channel.id})["number"]

        await ctx.channel.set_permissions(member, read_messages=True, send_messages=True, read_message_history=True)
        await ctx.channel.send(embed=discord.Embed(description=f'{memb.mention}, `к Вашему вопросу был добавлен пользователь:` {member.name}`(`{member.mention}`)`', colour=0xFB9E14, timestamp=datetime.datetime.utcnow()))
        try:
            await member.send(embed=discord.Embed(description=f'{member.mention}, `вы были добавлены к вопросу` **№{nmb}** `на сервере` **{ctx.guild.name}**.\n`Канал вопроса:` {ctx.channel.name}', colour=0xFB9E14, timestamp=datetime.datetime.utcnow()))
        except discord.Forbidden:
            pass
        add(ctx.guild.id, ctx.author, "addrep")

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def leave(self, ctx):
        if ctx.guild == None:
            return

        if not reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 1:
            return

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})

        if ctx.channel.id == rep["rchannel"]:
            return

        await ctx.message.delete()

        try:
            c1 = discord.utils.get(ctx.guild.categories, id = rep["category_id_two"])
            for i in c1.channels:
                await i.delete()
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.categories, id = rep["category_id_one"])
            for i in c1.channels:
                await i.delete()
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.categories, id = rep["category_id_three"])
            for i in c1.channels:
                await i.delete()
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.channels, id = rep["logchan"])
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.channels, id = rep["rchannel"])
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.roles, id = rep["support_role"])
            await c1.delete()
        except:
            pass

        try:
            if rep["start_channel"] > 0:
                c1 = discord.utils.get(ctx.guild.channels, id = rep["rchannel"])
                await c1.delete()
        except:
            pass

        loggeds = logged.find_one({"guild_id": ctx.guild.id})
        try:
            if loggeds["voicechannel"] > 1:
                await self.bot.get_channel(loggeds["voicechannel"]).delete()
        except:
            pass

        try:
            if loggeds["channelschannel"] > 1:
                await self.bot.get_channel(loggeds["channelschannel"]).delete()
        except:
            pass

        try:
            if loggeds["roleeditchannel"] > 1:
                await self.bot.get_channel(loggeds["roleeditchannel"]).delete()
        except:
            pass

        try:
            if loggeds["messagechannel"] > 1:
                await self.bot.get_channel(loggeds["messagechannel"]).delete()
        except:
            pass

        try:
            if loggeds["roleaddchannel"] > 1:
                await self.bot.get_channel(loggeds["roleaddchannel"]).delete()
        except:
            pass

        try:
            if loggeds["category"] > 1:
                await discord.utils.get(ctx.guild.categories, id = loggeds["category"]).delete()
        except:
            pass
        
        try:
            reports.delete_one({"guild_id": ctx.guild.id, "proverka": 3})
        except:
            pass

        for i in reports.find({"guild_id": ctx.guild.id}):
            reports.delete_one({"_id": i["_id"]})
        for i in moder.find({"guild": ctx.guild.id}):
            moder.delete_one({"_id": i["_id"]})
        logged.delete_one({"guild_id": ctx.guild.id})

        await ctx.guild.leave()

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def reload(self, ctx):
        if ctx.guild == None:
            return

        if not reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 1:
            return

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})

        if rep["start_channel"] > 0:
            return await ctx.send(embed = setembed(f'`Для использования этой команды закончите регистрацию в канале` <#{rep["start_channel"]}>', self.bot.user.avatar_url), delete_after = 10)

        if ctx.channel.id == rep["rchannel"]:
            return

        await ctx.message.delete()

        try:
            c1 = discord.utils.get(ctx.guild.categories, id = rep["category_id_two"])
            for i in c1.channels:
                await i.delete()
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.categories, id = rep["category_id_one"])
            for i in c1.channels:
                await i.delete()
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.categories, id = rep["category_id_three"])
            for i in c1.channels:
                await i.delete()
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.channels, id = rep["logchan"])
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.channels, id = rep["rchannel"])
            await c1.delete()
        except:
            pass

        try:
            c1 = discord.utils.get(ctx.guild.roles, id = rep["support_role"])
            await c1.delete()
        except:
            pass

        try:
            if rep["start_channel"] > 0:
                c1 = discord.utils.get(ctx.guild.channels, id = rep["rchannel"])
                await c1.delete()
        except:
            pass

        loggeds = logged.find_one({"guild_id": ctx.guild.id})
        try:
            if loggeds["voicechannel"] > 1:
                await self.bot.get_channel(loggeds["voicechannel"]).delete()
        except:
            pass

        try:
            if loggeds["channelschannel"] > 1:
                await self.bot.get_channel(loggeds["channelschannel"]).delete()
        except:
            pass

        try:
            if loggeds["roleeditchannel"] > 1:
                await self.bot.get_channel(loggeds["roleeditchannel"]).delete()
        except:
            pass

        try:
            if loggeds["messagechannel"] > 1:
                await self.bot.get_channel(loggeds["messagechannel"]).delete()
        except:
            pass

        try:
            if loggeds["roleaddchannel"] > 1:
                await self.bot.get_channel(loggeds["roleaddchannel"]).delete()
        except:
            pass

        try:
            if loggeds["category"] > 1:
                await discord.utils.get(ctx.guild.categories, id = loggeds["category"]).delete()
        except:
            pass

        logged.delete_one({"guild_id": ctx.guild.id})
        
        a, b, c, d = rep["vsego"], rep["active"], rep["close"], rep["number"]

        try:
            reports.delete_one({"guild_id": ctx.guild.id, "proverka": 3})
        except:
            pass

        for i in reports.find({"guild_id": ctx.guild.id}):
            reports.delete_one({"_id": i["_id"]})

        info = reports.find_one({"proverka": 2})
        channel = await ctx.guild.create_text_channel(f'репорт-бот-настройка', overwrites=None, reason= f'Перезагрузка системы(Командой !reload) | Выполнил: {ctx.author}')
        await channel.set_permissions(ctx.guild.default_role, read_messages = False)
        mes = await channel.send(embed = setembed(f'Вы ввели команду `!reload`, регистрация в базе данных началась сначала\n\n> `Мой создатель:` [{info["discord"]}]({info["vk"]})\n> `Сервер технической поддержки:` {info["server"]}\n\nСпасибо за то, что используете меня.\nДля начала работы со мной, нажмите на ▶', url = self.bot.user.avatar_url))
        await mes.add_reaction('▶')
        reports.insert_one({"guild_id": ctx.guild.id, "proverka": 1, "rchannel": "None", "category_id_one": 0, "category_id_two": 0, "category_id_three": 0, "number": d, "vsego": a, "close": c, "active": b, "himes": "None", "donate": 1, "last_name": "None", "channel": 0, "message_id": 0, "footer": "None", "image": "None", "logchan": 0, "prefix": "!", "support_role": 0, "start_channel": channel.id})
        logged.insert_one({"guild_id": ctx.guild.id, "voice": 0, "voicechannel": 0, "channels": 0, "channelschannel": 0, "roleedit": 0, "roleeditchannel": 0, "message": 0, "messagechannel": 0, "roleadd": 0, "roleaddchannel": 0, "category": 0})
        reports.insert_one({"guild_id": ctx.guild.id, "proverka": 3, "sender": 1, "ocenka": 1})

    @commands.command()
    async def imoder(self, ctx, member: discord.Member = None):
        if ctx.guild == None or ctx.guild.id in [477547500232769536, 664111470782578708]:
            return

        if not reports.count_documents({"guild_id": ctx.guild.id, "proverka": 1}) == 1:
            return
            
        await ctx.message.delete()

        if member == None:
            member = ctx.author

        rep = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})
        if rep["start_channel"] > 0:
            return await ctx.send(embed = setembed(f'Для начала работы со мной, необходимо пройти регистрацию в базе данных.\n`Закончите регистрацию в канале` <#{rep["start_channel"]}>\n\n**Если произошла ошибка и необходимо пройти регистрацию заново, введите `!reload`**', self.bot.user.avatar_url), delete_after = 10)

        if not discord.utils.get(ctx.guild.roles, id = rep["support_role"]) in ctx.author.roles:
            return

        if not discord.utils.get(ctx.guild.roles, id = rep["support_role"]) in member.roles:
            return await ctx.send(embed = setembed(f'Данный пользователь не является агентом технической поддержки.\n`[P.S]: У него нет роли` <@&{rep["support_role"]}>', self.bot.user.avatar_url), delete_after = 5)

        if moder.count_documents({"guild": ctx.guild.id, "id": member.id}) == 0:
            moder.insert_one({"guild": ctx.guild.id, "id": member.id, "close": 0, "rasm": 0, "repa": 0, "addme": 0, "addrep": 0})
            embed = discord.Embed(title = f'Статистика модератора 📍 {member}', description = f'**👁️ Всего действий от него: `0`**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
            embed.add_field(name = '❔ | `Статистика вопросов`', value = f'> 🔹 `Принято вопросов:` **0**\n> 🔹 `Закрыто вопросов:` **0**\n> 🔹 `Поставлено на рассмотрение:` **0**\n> 🔹 `Добавлено людей к репортам:` **0**\n\n> ➕ `Репутация:` **0**', inline = False)
            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
            return await ctx.send(embed = embed)

        if ctx.channel.id == rep["rchannel"]:
            return


        info = reports.find_one({"proverka": 2})
        if rep["donate"] == 0:
            return await ctx.send(embed = setembed(f'**Это платная функция, для её приобретения необходимо написать разработчику**\n\n> `Мой создатель:` [{info["discord"]}]({info["vk"]})\n> `Сервер технической поддержки:` {info["server"]}\n\nСпасибо за то, что используете меня ❤', self.bot.user.avatar_url), delete_after = 10)
            
        i = []
        ms = ['close', 'rasm', 'repa', 'addme', 'addrep']
        for b in ms:
            i.append(moder.find_one({"guild": ctx.guild.id, "id": member.id})[b])
        
        foc = int(i[0]) + int(i[1]) + int(i[2]) + int(i[3]) + int(i[4])
        embed = discord.Embed(title = f'Статистика модератора 📍 {member}', description = f'**👁️ Всего действий от него: `{foc}`**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        embed.add_field(name = '❔ | `Статистика вопросов`', value = f'> 🔹 `Принято вопросов:` **{i[0]}**\n> 🔹 `Закрыто вопросов:` **{i[0]}**\n> 🔹 `Поставлено на рассмотрение:` **{i[1]}**\n> 🔹 `Добавлено людей к репортам:` **{i[4]}**\n\n> ➕ `Репутация:` **{i[2]}**', inline = False)
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(report(bot))

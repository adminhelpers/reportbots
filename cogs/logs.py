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
logged = db["logs"]
reports = db["reports"]


class logs(commands.Cog):
    """LOGS Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Logs by dollar ム baby#3603 - Запущен')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):

        if member.guild == None:
            return

        if logged.count_documents({"guild_id": member.guild.id}) == 0:
            return

        log = logged.find_one({"guild_id": member.guild.id})

        if log["voice"] == 0:
            return

        if after.channel == None:
            if not before.channel == None:
                if member.bot:
                    return
                channel = self.bot.get_channel(log["voicechannel"])
                e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) вышел из голосового канала 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Выход из канала', icon_url = self.bot.user.avatar_url)
                e.add_field(name = "Предыдущий канал", value = f"**{before.channel.name}({before.channel.mention})**")
                e.add_field(name = "ID Участника", value = f"**{member.id}**")
                e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                try:
                    return await channel.send(embed = e)
                except:
                    pass

        if (not before.channel == None) and (not after.channel == None):
            if before.channel.id == after.channel.id:
                return

            if member.bot:
                return
            channel = self.bot.get_channel(log["voicechannel"])
            e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) перешёл в другой голосовой канал 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = f'Журнал аудита | Переход в канал', icon_url = self.bot.user.avatar_url)
            e.add_field(name = "Действующий канал", value = f"**{after.channel.name}({after.channel.mention})**")
            e.add_field(name = "Предыдущий канал", value = f"**{before.channel.name}({before.channel.mention})**")
            e.add_field(name = "ID Участника", value = f"**{member.id}**")
            e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
            try:
                return await channel.send(embed = e)
            except:
                pass

        if not after.channel == None:
            if before.channel == None:
                if member.bot:
                    return
                channel = self.bot.get_channel(log["voicechannel"])
                e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) зашёл в голосовой канал 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Вход в канал', icon_url = self.bot.user.avatar_url)
                e.add_field(name = "Действующий канал", value = f"**{after.channel.name}({after.channel.mention})**")
                e.add_field(name = "ID Участника", value = f"**{member.id}**")
                e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                try:
                    return await channel.send(embed = e)
                except:
                    pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        if channel.guild == None:
            return

        if logged.count_documents({"guild_id": channel.guild.id}) == 0:
            return

        log = logged.find_one({"guild_id": channel.guild.id})

        if log["channels"] == 0:
            return

        chanel = self.bot.get_channel(log["channelschannel"])
        async for entry in channel.guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_create):
            if entry.user.bot:
                return
            e = discord.Embed(colour = entry.user.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Журнал аудита | Создание канала', icon_url = self.bot.user.avatar_url)
            e.add_field(name = "Канал:", value = f"<#{entry.target.id}>")
            e.add_field(name = "ID Канала:", value = f"{entry.target.id}")
            e.add_field(name = "Создал:", value = f"{entry.user.mention}")
            e.add_field(name = "ID создавшего:", value = f"{entry.user.id}")
            e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
            try:
                return await chanel.send(embed = e)
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):

        if channel.guild == None:
            return

        if logged.count_documents({"guild_id": channel.guild.id}) == 0:
            return

        log = logged.find_one({"guild_id": channel.guild.id})

        if log["channels"] == 0:
            return

        chanel = self.bot.get_channel(log["channelschannel"])
        async for entry in channel.guild.audit_logs(action = discord.AuditLogAction.channel_delete):
            if entry.user.bot:
                return
            e = discord.Embed(colour = entry.user.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Журнал аудита | Удаление канала', icon_url = self.bot.user.avatar_url)
            e.add_field(name = "Канал:", value = f"{channel.name}")
            e.add_field(name = "ID Канала:", value = f"{entry.target.id}")
            e.add_field(name = "Удалил:", value = f"{entry.user.mention}")
            e.add_field(name = "ID удалившего:", value = f"{entry.user.id}")
            e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
            try:
                return await chanel.send(embed = e)
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):

        if role.guild == None:
            return

        if logged.count_documents({"guild_id": role.guild.id}) == 0:
            return

        log = logged.find_one({"guild_id": role.guild.id})

        if log["roleedit"] == 0:
            return

        chanel = self.bot.get_channel(log["roleeditchannel"])
        async for entry in chanel.guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_create):
            e = discord.Embed(colour = role.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Журнал аудита | Создание роли', icon_url = self.bot.user.avatar_url)
            e.add_field(name = "Роль:", value = f"<@&{entry.target.id}>")
            e.add_field(name = "ID роли:", value = f"{entry.target.id}")
            e.add_field(name = "Создал:", value = f"{entry.user.mention}")
            e.add_field(name = "ID создавшего:", value = f"{entry.user.id}")
            e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
            try:
                return await chanel.send(embed = e)
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):

        if role.guild == None:
            return

        if logged.count_documents({"guild_id": role.guild.id}) == 0:
            return

        log = logged.find_one({"guild_id": role.guild.id})

        if log["roleedit"] == 0:
            return

        chanel = self.bot.get_channel(log["roleeditchannel"])
        async for entry in chanel.guild.audit_logs(action = discord.AuditLogAction.role_delete):
            e = discord.Embed(colour = role.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Журнал аудита | Удаление роли', icon_url = self.bot.user.avatar_url)
            e.add_field(name = "Роль:", value = f"{role.name}")
            e.add_field(name = "ID роли:", value = f"{entry.target.id}")
            e.add_field(name = "Удалил:", value = f"{entry.user.mention}")
            e.add_field(name = "ID удалившего:", value = f"{entry.user.id}")
            e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
            try:
                return await chanel.send(embed = e)
            except:
                pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild == None:
            return

        if message.author.bot:
            return

        if logged.count_documents({"guild_id": message.guild.id}) == 0:
            return

        log = logged.find_one({"guild_id": message.guild.id})

        if log["message"] == 0:
            return

        channel = self.bot.get_channel(log["messagechannel"])
        e = discord.Embed(colour = message.author.color, timestamp = datetime.datetime.utcnow())
        e.set_author(name = f'Журнал аудита | Удаление сообщения', icon_url = self.bot.user.avatar_url)
        e.add_field(name = "Удалённое сообщение", value = f"```{message.content}```")
        e.add_field(name = "Автор", value = f"**{message.author.display_name}({message.author.mention})**")
        e.add_field(name = "Канал", value = f"**{message.channel.mention}**")
        e.add_field(name = "ID Сообщения", value = f"**{message.id}**")
        e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
        try:
            return await channel.send(embed = e)
        except:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if before.guild == None:
            return
        
        if before.content == after.content:
            return

        if before.author.bot:
            return

        if logged.count_documents({"guild_id": after.guild.id}) == 0:
            return

        log = logged.find_one({"guild_id": after.guild.id})

        if log["message"] == 0:
            return

        channel = self.bot.get_channel(log["messagechannel"])
        e = discord.Embed(description = f'**[Сообщение]({before.jump_url}) было изменено.**', colour = before.author.color, timestamp = datetime.datetime.utcnow())
        e.set_author(name = f'Журнал аудита | Изменение сообщения', icon_url = self.bot.user.avatar_url)
        e.add_field(name = "Старое содержимое", value = f"```{before.content}```")
        e.add_field(name = "Новое соодержиое", value = f"```{after.content}```")
        e.add_field(name = "Автор", value = f"**{before.author.display_name}({before.author.mention})**")
        e.add_field(name = "Канал", value = f"**{before.channel.mention}**")
        e.add_field(name = "ID Сообщения", value = f"**{before.id}**")
        e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
        try:
            return await channel.send(embed = e)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild == None:
            return

        if logged.count_documents({"guild_id": after.guild.id}) == 0:
            return

        log = logged.find_one({"guild_id": after.guild.id})

        if log["roleadd"] == 0:
            return

        if not len(before.roles) == len(after.roles):
            
            role = [ ]
            if len(before.roles) > len(after.roles):
                for i in before.roles:
                    if not i in after.roles:                                 
                            if not i.id == before.guild.default_role.id:
                                role.append(f'➖ Была убрана роль {i.name}(<@&{i.id}>)\n')
            elif len(before.roles) < len(after.roles):
                    for i in after.roles:
                        if not i in before.roles:
                            if not i.id == before.guild.default_role.id:
                                role.append(f'➕ Была добавлена роль {i.name}(<@&{i.id}>)\n')

            if not before.display_name == after.display_name:
                channel = self.bot.get_channel(log["roleaddchannel"])
                e = discord.Embed(description = f'**Пользователь {before.name}({after.mention}) изменил NickName**', colour = before.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Изменение NickName участника', icon_url = self.bot.user.avatar_url)
                e.add_field(name = "Действующее имя", value = f"**{after.display_name}({after.mention})**")
                e.add_field(name = "Предыдущее имя", value = f"**{before.display_name}({before.mention})**")
                e.add_field(name = "ID Участника", value = f"**{after.id}**")
                e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                try:
                    return await channel.send(embed = e)
                except:
                    pass
            else:
                str_a = ''.join(role)
                channel = self.bot.get_channel(log["roleaddchannel"])
                e = discord.Embed(description = f'**У пользователя {after.name}({after.mention}) были изменены роли.**', colour = before.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Изменение ролей участника', icon_url = self.bot.user.avatar_url)
                e.add_field(name = "Было сделано", value = f"**{str_a}**")
                e.add_field(name = "ID Участника", value = f"**{after.id}**")
                e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                try:
                    return await channel.send(embed = e)
                except:
                    pass


def setup(bot):
    bot.add_cog(logs(bot))

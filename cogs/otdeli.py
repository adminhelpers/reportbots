import discord
from discord.ext import commands
import json
import asyncio
import sqlite3
import re
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
moder = db["moder"]
warns = db["warns"]
otdl = db["otdeli"]

class otdels(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.prev = []

  @commands.Cog.listener()
  async def on_ready(self):
    print('+')

  @commands.command(aliases = ['добавить', 'addotdel'])
  async def dete(self, ctx, otdel:int = None, nick = None):
    await ctx.message.delete()

    if otdel is None:
      return await ctx.channel.send('`[ERROR]` `Обязательно укажите номер отдела!`', embed = discord.Embed(description = f'**/добавить** [Номер отдела(1-3)] [Nick_Name**(Обязательно слитно)**]', colour = 0xFB9E14), delete_after = 10)

    if nick is None:
      return await ctx.channel.send('`[ERROR]` `Обязательно укажите ник человека(Обязательно слитно)!`', embed = discord.Embed(description = f'**/добавить** [Номер отдела(1-3)] [Nick_Name**(Обязательно слитно)**]', colour = 0xFB9E14), delete_after = 10)

    s = 0
    if discord.utils.get(ctx.guild.roles, id = 757589805742817280) in ctx.author.roles or discord.utils.get(ctx.guild.roles, id = 757589876492337202) in ctx.author.roles: # lider и zam
      s = 1
    elif discord.utils.get(ctx.guild.roles, id = 757589849745129473) in ctx.author.roles or discord.utils.get(ctx.guild.roles, id = 757589816383766603) in ctx.author.roles: #gs и zgs
      s = 1
    elif discord.utils.get(ctx.guild.roles, id = 757589833387475034) in ctx.author.roles: #следящий
      s = 1

    if s == 0:
      return await ctx.send('`[ERROR]` `Отказано в доступе!`', delete_after = 5)

    otd = {
      757601780409434183: 760874267407024180,
      757601726592450651: 760874121604104202,
      757601797077598329: 760874578879840306,
      757601792472252567: 760874805226111046,
      758648331667898388: 760875032313462804,
      757601794959474808: 760875237071126541,
      757601748843233341: 760875428008689666,
      757601735706542163: 760875654328745984,
      757601779339886612: 760875843249111066,
      757601727636701366: 760876076976570469,
      758031284135264376: 760876285605707797,
      757601738177118328: 760876526643314771,
      758012902257983548: 760876732382969879
    }

    channelsf = {
      757601726592450651: 'Правительство',
      757601780409434183: 'Сбербанк',
      757601797077598329: 'ГУВД г.Арзамаса',
      757601792472252567: 'УВД г.Эдово',
      758648331667898388: 'УВД г.Лыткарино',
      757601794959474808: 'Федеральная Служба Безопасности',
      757601748843233341: 'Федеральная Служба Исполнения Наказаний',
      757601735706542163: 'Министерство Обороны',
      757601779339886612: 'Больница г.Арзамас',
      757601727636701366: 'Больница г.Эдово',
      758031284135264376: 'Главное Военное-Медицинское Управление',
      757601738177118328: 'Новостное Агенство "Дождь"',
      758012902257983548: 'Радиостанция "Рокс"'
    }

    rolek = {
      757601726592450651: 757589893131010049,
      757601780409434183: 757589904887906424,
      757601797077598329: 757589846704259114,
      757601792472252567: 757589892103536652,
      758648331667898388: 757589890153316434,
      757601794959474808: 757589821320593521,
      757601748843233341: 757589861388648448,
      757601735706542163: 757589801812754462,
      757601779339886612: 757589897858121829,
      757601727636701366: 757589870620442764,
      758031284135264376: 757589815582523443,
      757601738177118328: 757589806573158460,
      758012902257983548: 757589884851585150
    }

    eq = otd.get(ctx.channel.id, None)
    if eq is None:
      return await ctx.send('`[ERROR]` `В данном канале не обнаружено сообщения с информацией о отделах!`', delete_after = 5)
    
    if not discord.utils.get(ctx.guild.roles, id = rolek[ctx.channel.id]) in ctx.author.roles:
      return await ctx.send('`[ERROR]` `Вы не имеете доступа к редактированию отделов этого канала!`', delete_after = 5)

    if len(nick) <= 3:
      return await ctx.send('`[ERROR]` `Ник должен иметь более 6-ти символов!`', delete_after = 5)

    if not otdel in [1, 2, 3]:
        return await ctx.send('`[ERROR]` `Такого отдела не существует.`')
    
    if otdl.count_documents({"mid": ctx.channel.id}) == 0:
        otdl.insert_one({"mid": ctx.channel.id, "onename": "one", "twoname": "two", "threename": "three", "one": 0, "three": 0, "two": 0})

    otdels = {
      1: 'onename',
      2: 'twoname',
      3: 'threename'
    }

    otdelss = {
      1: 'one',
      2: 'two',
      3: 'three'
    }
    
    notdel = otdelss[otdel]
    for i in otdl.find({"mid": ctx.channel.id}):
      if i[notdel] == 0:
          otdl.update_one({"mid": ctx.channel.id}, {"$set": {notdel: f'{nick}\n'}})
      else:
        ath = re.findall(r'\w*', otdl.find_one({"mid": ctx.channel.id})[notdel])
        if nick in ath:
            return await ctx.send('`[ERROR]` `Этот человек уже внесён в список!`', delete_after = 5)
        else:
            otdl.update_one({"mid": ctx.channel.id}, {"$set": {notdel: f'{otdl.find_one({"mid": ctx.channel.id})[notdel]}{nick}\n'}})    

    message = await ctx.channel.fetch_message(otd.get(ctx.channel.id, None))
    embed = discord.Embed(title = 'Отделы', description = f'**Фракционные отделы фракции `{channelsf[ctx.channel.id]}`\nУзнать команды для работы с этим сообщением можно по команде: `/ohelp`**', colour = 0xFB9E14)
    chel1 = otdl.find_one({"mid": ctx.channel.id})["one"]
    chel2 = otdl.find_one({"mid": ctx.channel.id})["two"]
    chel3 = otdl.find_one({"mid": ctx.channel.id})["three"]
    if chel1 == 0 or len(chel1) <= 4:
        chel1 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["onename"], value = f'`{chel1}`', inline = False)
    if chel2 == 0 or len(chel2) <= 4:
        chel2 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["twoname"], value = f'`{chel2}`', inline = False)
    if chel3 == 0 or len(chel3) <= 4:
        chel3 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["threename"], value = f'`{chel3}`', inline = False)

    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)

    await message.edit(content = None, embed = embed)
    await ctx.send(f'`[TRY]` `Пользователь {nick} был добавлен в список отдела {otdel}!`\n`Для того что бы убрать человека из списка используйте:`', embed = discord.Embed(description = '**/delotdel** [название отдела] [Имя_Человека(Обязательно слитно)]', colour = 0xFB9E14), delete_after = 30)

  @commands.command(aliases = ['название', 'setotdel'])
  async def setotdelname(self, ctx, otdel:int = None, *, nick = None):
    
    await ctx.message.delete()

    if nick is None:
      return await ctx.channel.send('`[ERROR]` `Обязательно укажите устанавливаемое название отдела!`', embed = discord.Embed(description = f'**/название** [Номер отдела(1-3)] [Новое название]', colour = 0xFB9E14), delete_after = 10)

    if otdel is None:
      return await ctx.channel.send('`[ERROR]` `Обязательно укажите номер редактируемого отдела!`', embed = discord.Embed(description = f'**/название** [Номер отдела(1-3)] [Новое название]', colour = 0xFB9E14), delete_after = 10)

    lidrol = discord.utils.get(ctx.guild.roles, id = 757589805742817280)
    if not lidrol in ctx.author.roles:
      return await ctx.send('`[ERROR]` `Отказано в доступе!`', delete_after = 5)

    otd = {
      757601780409434183: 760874267407024180,
      757601726592450651: 760874121604104202,
      757601797077598329: 760874578879840306,
      757601792472252567: 760874805226111046,
      758648331667898388: 760875032313462804,
      757601794959474808: 760875237071126541,
      757601748843233341: 760875428008689666,
      757601735706542163: 760875654328745984,
      757601779339886612: 760875843249111066,
      757601727636701366: 760876076976570469,
      758031284135264376: 760876285605707797,
      757601738177118328: 760876526643314771,
      758012902257983548: 760876732382969879
    }

    channelsf = {
      757601726592450651: 'Правительство',
      757601780409434183: 'Сбербанк',
      757601797077598329: 'ГУВД г.Арзамаса',
      757601792472252567: 'УВД г.Эдово',
      758648331667898388: 'УВД г.Лыткарино',
      757601794959474808: 'Федеральная Служба Безопасности',
      757601748843233341: 'Федеральная Служба Исполнения Наказаний',
      757601735706542163: 'Министерство Обороны',
      757601779339886612: 'Больница г.Арзамас',
      757601727636701366: 'Больница г.Эдово',
      758031284135264376: 'Главное Военное-Медицинское Управление',
      757601738177118328: 'Новостное Агенство "Дождь"',
      758012902257983548: 'Радиостанция "Рокс"'
    }

    rolek = {
      757601726592450651: 757589893131010049,
      757601780409434183: 757589904887906424,
      757601797077598329: 757589846704259114,
      757601792472252567: 757589892103536652,
      758648331667898388: 757589890153316434,
      757601794959474808: 757589821320593521,
      757601748843233341: 757589861388648448,
      757601735706542163: 757589801812754462,
      757601779339886612: 757589897858121829,
      757601727636701366: 757589870620442764,
      758031284135264376: 757589815582523443,
      757601738177118328: 757589806573158460,
      758012902257983548: 757589884851585150
    }

    eq = otd.get(ctx.channel.id, None)
    if eq is None:
      return await ctx.send('`[ERROR]` `В данном канале не обнаружено сообщения с информацией о отделах!`', delete_after = 5)

    
    if not discord.utils.get(ctx.guild.roles, id = rolek[ctx.channel.id]) in ctx.author.roles:
      return await ctx.send('`[ERROR]` `Вы не имеете доступа к редактированию отделов этого канала!`', delete_after = 5)

    if not otdel in [1, 2, 3]:
        return await ctx.send('`[ERROR]` `Такого отдела не существует.`')

    otdels = {
      1: 'onename',
      2: 'twoname',
      3: 'threename'
    }

    notdel = otdels[otdel]

    if otdl.count_documents({"mid": ctx.channel.id}) == 0:
        otdl.insert_one({"mid": ctx.channel.id, "onename": "one", "twoname": "two", "threename": "three", "one": 0, "three": 0, "two": 0})
        otdl.update_one({"mid": ctx.channel.id}, {"$set": {notdel: nick}})
    else:
        otdl.update_one({"mid": ctx.channel.id}, {"$set": {notdel: nick}})

    message = await ctx.channel.fetch_message(otd.get(ctx.channel.id, None))
    embed = discord.Embed(title = 'Отделы', description = f'**Фракционные отделы фракции `{channelsf[ctx.channel.id]}`\nУзнать команды для работы с этим сообщением можно по команде: `/ohelp`**', colour = 0xFB9E14)
    chel1 = otdl.find_one({"mid": ctx.channel.id})["one"]
    chel2 = otdl.find_one({"mid": ctx.channel.id})["two"]
    chel3 = otdl.find_one({"mid": ctx.channel.id})["three"]
    if chel1 == 0 or len(chel1) <= 4:
        chel1 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["onename"], value = f'`{chel1}`', inline = False)
    if chel2 == 0 or len(chel2) <= 4:
        chel2 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["twoname"], value = f'`{chel2}`', inline = False)
    if chel3 == 0 or len(chel3) <= 4:
        chel3 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["threename"], value = f'`{chel3}`', inline = False)

    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)

    await message.edit(content = None, embed = embed)
    await ctx.send(f'`[ACCEPT]` `Новое название отдела успешно установлено!`\n`Логирование:`', embed = discord.Embed(description = f'**Номер отдела:** {otdel}\n**Новое название отдела:** {nick}\n**Изменил:** {ctx.author.display_name}', colour = 0xFB9E14), delete_after = 60)
      

  @commands.command(aliases = ['убрать', 'delotdel'])
  async def undete(self, ctx, otdel: int = None, nick = None):

    await ctx.message.delete()

    if otdel is None:
      return await ctx.channel.send('`[ERROR]` `Обязательно укажите номер отдела!`', embed = discord.Embed(description = f'**/убрать** [Номер отдела(1-3)] [Nick_Name**(Обязательно слитно)**]', colour = 0xFB9E14), delete_after = 10)

    if nick is None:
      return await ctx.channel.send('`[ERROR]` `Обязательно укажите ник человека(Обязательно слитно)!`', embed = discord.Embed(description = f'**/убрать** [Номер отдела(1-3)] [Nick_Name**(Обязательно слитно)**]', colour = 0xFB9E14), delete_after = 10)

    otd = {
      757601780409434183: 760874267407024180,
      757601726592450651: 760874121604104202,
      757601797077598329: 760874578879840306,
      757601792472252567: 760874805226111046,
      758648331667898388: 760875032313462804,
      757601794959474808: 760875237071126541,
      757601748843233341: 760875428008689666,
      757601735706542163: 760875654328745984,
      757601779339886612: 760875843249111066,
      757601727636701366: 760876076976570469,
      758031284135264376: 760876285605707797,
      757601738177118328: 760876526643314771,
      758012902257983548: 760876732382969879
    }

    channelsf = {
      757601726592450651: 'Правительство',
      757601780409434183: 'Центральный Банк',
      757601797077598329: 'ГУВД г.Арзамаса',
      757601792472252567: 'УВД г.Эдово',
      758648331667898388: 'УВД г.Лыткарино',
      757601794959474808: 'Федеральная Служба Безопасности',
      757601748843233341: 'Федеральная Служба Исполнения Наказаний',
      757601735706542163: 'Министерство Обороны',
      757601779339886612: 'Больница г.Арзамас',
      757601727636701366: 'Больница г.Эдово',
      758031284135264376: 'Главное Военное-Медицинское Управление',
      757601738177118328: 'Новостное Агенство "Дождь"',
      758012902257983548: 'Радиостанция "Рокс"'
    }

    rolek = {
      757601726592450651: 757589893131010049,
      757601780409434183: 757589904887906424,
      757601797077598329: 757589846704259114,
      757601792472252567: 757589892103536652,
      758648331667898388: 757589890153316434,
      757601794959474808: 757589821320593521,
      757601748843233341: 757589861388648448,
      757601735706542163: 757589801812754462,
      757601779339886612: 757589897858121829,
      757601727636701366: 757589870620442764,
      758031284135264376: 757589815582523443,
      757601738177118328: 757589806573158460,
      758012902257983548: 757589884851585150
    }

    otdels = {
      1: 'one',
      2: 'two',
      3: 'three'
    }

    lidrol = discord.utils.get(ctx.guild.roles, id = 757589805742817280)
    if not lidrol in ctx.author.roles:
      return await ctx.send('`[ERROR]` `Отказано в доступе!`', delete_after = 5)

    eq = otd.get(ctx.channel.id, None)
    if eq is None:
      return await ctx.send('`[ERROR]` `В данном канале не обнаружено сообщения с информацией о отделах!`', delete_after = 5)
    
    if not discord.utils.get(ctx.guild.roles, id = rolek[ctx.channel.id]) in ctx.author.roles:
      return await ctx.send('`[ERROR]` `Вы не имеете доступа к редактированию отделов этого канала!`', delete_after = 5)

    if otdl.count_documents({"mid": ctx.channel.id}) == 0:
        return await ctx.send('`[ERROR]` `Данного пользователя нет в списке.`', delete_after = 5)

    if not otdel in [1, 2, 3]:
      return await ctx.send('`[ERROR]` `Такого отдела не существует!`', delete_after = 5)


    notdel = otdels[otdel]
    for i in otdl.find({"mid": ctx.channel.id}):
        if i[notdel] == 0:
            return await ctx.send('`[ERROR]` `Этот человека нет в списке!`', delete_after = 5)
        else:
            ath = re.findall(r'\w*', otdl.find_one({"mid": ctx.channel.id})[notdel])
            if not nick in ath:
                return await ctx.send('`[ERROR]` `Этот человека нет в списке!`', delete_after = 5)
            else:
                result = []
                for j in ath:
                    if not j == nick and len(j) >= 1:
                        result.append(f'{j}\n')
                amas = ''.join(result)
                otdl.update_one({"mid": ctx.channel.id}, {"$set": {notdel: amas}})  
                await ctx.send(f'`[ACCEPT]` `Ник {nick} успешно удалён из списка сотрудников отдела {otdel}`', delete_after = 30)   

    message = await ctx.channel.fetch_message(otd.get(ctx.channel.id, None))
    embed = discord.Embed(title = 'Отделы', description = f'**Фракционные отделы фракции `{channelsf[ctx.channel.id]}`\nУзнать команды для работы с этим сообщением можно по команде: `/ohelp`**', colour = 0xFB9E14)
    chel1 = otdl.find_one({"mid": ctx.channel.id})["one"]
    chel2 = otdl.find_one({"mid": ctx.channel.id})["two"]
    chel3 = otdl.find_one({"mid": ctx.channel.id})["three"]
    if chel1 == 0 or len(chel1) <= 4:
        chel1 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["onename"], value = f'`{chel1}`', inline = False)
    if chel2 == 0 or len(chel2) <= 4:
        chel2 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["twoname"], value = f'`{chel2}`', inline = False)
    if chel3 == 0 or len(chel3) <= 4:
        chel3 = '-'
    embed.add_field(name = otdl.find_one({"mid": ctx.channel.id})["threename"], value = f'`{chel3}`', inline = False)

    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)

    await message.edit(content = None, embed = embed)

  @commands.command()
  async def ohelp(self, ctx):
    if not ctx.guild.id == 325607843547840522:
      return

    await ctx.message.delete()

    embed = discord.Embed(title = 'Команды', description = f'**🎮 В данном дискорде действует система "Отделы".\nВ разделе каждой госудаственной структуры находится сообщение с отделами, в которые лидер может заносить и выносить людей.\nКоманды распространяющиеся на эту систему доступны только лидерам своих фракций!**', colour = 0xFB9E14)
    embed.add_field(name = '❔ | `Нумерация отделов`', value = f'**Все отделы идут в порядке номеров от 1 до 3\nПорядок расположения: Сверху - Вниз\nПри редактировании отдела, добавления или удаления из него участников, аргументом отдело, вне зависимости от названия, должны быть цыфры от 1 до 3**', inline = False)
    embed.add_field(name = '📌 | `Добавить пользователя в список`', value = f'**Необходимые аргументы:\n> `Номер отдела и Ник пользователя который должен писаться слитно`\nПример исполнения команды:\n> `/добавить 3 William_Taykus`\n-- Я добавлю ник William_Taykus в список ников 3-го отдела\n> `/добавить 3 Mark Markul`\n-- Я добавлю ник Mark в список ников 3-го отдела**', inline = False)
    embed.add_field(name = '🔧 | `Убрать пользователя из списка`', value = f'**Необходимые аргументы:\n> `Номер отдела и Ник пользователя который должен писаться слитно`\nПример исполнения команды:\n> `/убрать 2 William_Taykus`\n-- Я уберу ник William_Taykus из списка ников 2-го отдела**', inline = False)
    embed.add_field(name = '✏ | `Изменить название отдела`', value = f'**Необходимые аргументы:\n> `Номер отдела и новое название`\nПример исполнения команды:\n> `/название 2 Отдел Юстиции`\n-- Я установлю второму отделу название "Отдел Юстиции"**', inline = False)
    embed.set_thumbnail(url = ctx.guild.icon_url)
    embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
    return await ctx.send(embed = embed, delete_after = 50)

def setup(bot):
    bot.add_cog(otdels(bot))
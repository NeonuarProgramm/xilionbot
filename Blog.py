import discord, random # Импортирование библиотеки
from discord.voice_client import VoiceClient
import datetime # Импортирование ДатаТайм
import nekos # имопртируем новую библиотеку 
import random
import json
from discord import Status
from itertools import cycle
from discord.utils import get
from os import system
import sqlite3
import traceback
import os
import shutil
import anime
import asyncio
import math
import itertools
from discord.ext import commands # Импортирование commads из discord.ext

Bot = commands.Bot(command_prefix='x!') # Переменная бота, тут вводите префикс какой вы хотите
Bot.remove_command('help') # Убирает стандартную команду help

def postfix(num:int, end_1:str='год', end_2:str='года', end_3:str='лет'): # Функция обработрки постфикса
    num = num % 10 if num > 20 else num # Делим число на 10 и получаем то что осталось после деления, дальше проверка это больше чем 20 или нет, если больше то оставляем число не изменныс, а если меньше то заменяем число на остаток деления
    return end_1 if num == 1 else end_2 if 1 < num < 5 else end_3 # Тут уже просто прлверяем

# Clear message
@Bot.command( pass_context = True )

async def clear( ctx, amount = 100):
    await ctx.channel.purge( limit = amount )

@Bot.event # Ивент
async def on_ready(): # Тут пишите тип ивента, в нашем случие on_ready, то есть, наш бот будет это выполнять при запуске
    print(f"[SYSTEM] Bot online!\n[SYSTEM] Name - {Bot.user}\n[SYSTEM] ID - {Bot.user.id}\n[SYSTEM] Status - Active\n[SYSTEM] General Server - Xilya|Team 2.0") # Выводит текст с данными бота
    game = discord.Game(f"x!help | Ксилион")
    await Bot.change_presence(status=discord.Status.online, activity= game)

@Bot.command() # Декоратор команды
async def ping(ctx): # # Название команды
    emb = discord.Embed( # Переменная ембеда
        title= 'Текущий пинг', # Заполняем заголовок
        description= f'{Bot.ws.latency * 1000:.0f} ms' # Запонлняем описание
    )
    await ctx.send(embed=emb) # Отпрвака ембеда


@Bot.command() # Декоратор команды
async def avatar(ctx, member : discord.Member = None): # Название команды и аргументы
    user = ctx.message.author if member == None else member # Проверка аргуменат и переменная участника
    emb = discord.Embed( # Переменная ембеда
        title=f'Аватар пользователя {user}', # Заполняем заголовок
        description= f'[Ссылка на изображение]({user.avatar_url})', # Запонлняем описание
        color=user.color # Устанавливаем цвет
    )
    emb.set_image(url=user.avatar_url) # Устанавливаем картинку
    await ctx.send(embed=emb) # Отпрвака ембеда


@Bot.command() # Декоратор команды
async def servercount(ctx): # Название команды
    await ctx.send(f'Бот установлен на {len(Bot.guilds)} серверах') # Выводит кол-во серверов бота


@Bot.command() # Декоратор команды
async def knb(ctx, move: str = None): # Название команды и аргумент
    solutions = ["`ножницы`", "`камень`", "`бумага`", "`ножници`", "`камен`", "`бумаг`", "`ножниці`"] # Варианты хода
    winner = "**Ничья**" # Тут все понятно
    p1 = solutions.index(f"`{move.lower()}`") # Тут мы ищем номер хода пользователя
    p2 = random.randint(0, 2) # Ну тут бот "делает ход"
    if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0: # Проверка комбинации проигрыша
        winner = f"{ctx.message.author.mention} Ваш результат **Проиграл**"
    elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:  # Проверка комбинации выигрыша
        winner = f"{ctx.message.author.mention} Ваш результат **Выиграл**"
    await ctx.send(f"{ctx.message.author.mention} **-** {solutions[p1]}\n{Bot.user.mention} **-** {solutions[p2]}\n{winner}") # Отправка результатов


@Bot.command() # Декоратор команды
async def profile(ctx, userf: discord.Member = None): # Название команды и аргумент
    user = ctx.message.author if userf == None else userf # Проверка указан ли пользователь, если нет то заменяем автором команды
    status = user.status # Получаем статус

    if user.is_on_mobile() == True: stat = 'На телефоне' # Проверка статуса и указываем статус
    if status == discord.Status.online: stat = 'В сети' # Проверка статуса и указываем статус
    elif status == discord.Status.offline: stat = 'Не в сети' # Проверка статуса и указываем статус
    elif status == discord.Status.idle: stat = 'Не активен' # Проверка статуса и указываем статус
    elif status == discord.Status.dnd: stat = 'Не беспокоить' # Проверка статуса и указываем статус

    create_time = (datetime.datetime.today()-user.created_at).days # Узнаем кол-во дней в дискорде
    join_time = (datetime.datetime.today()-user.joined_at).days # Узнаем кол-во дней на сервере

    emb = discord.Embed(title='Профиль', colour= user.color) # Делаем ембед и устанавливаем цвет
    emb.add_field(name= 'Ник', value= user.display_name, inline= False) # Добавляем поле и заполняем 
    emb.add_field(name= 'ID', value= user.id, inline= False) # Добавляем поле и заполняем 
    
    if create_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни в дискорде
    else:
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( {create_time} {postfix(create_time, "день", "дня", "дней")})', inline= False)# Добавляем поле и заполняем кол-во дней в дискорде и подбираем окончание
    if join_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни на сервере
    else:
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( {join_time} {postfix(join_time, "день", "дня", "дней")} )', inline= False) # Добавляем поле и заполняем кол-во дней на сервере и подбираем окончание
    emb.add_field(name= 'Наивысшая роль', value= f"<@&{user.top_role.id}>", inline= False) # Добавляем поле и заполняем роль
    emb.add_field(name= 'Статус', value= stat, inline= False) # Добавляем поле и заполняем статус
    emb.set_thumbnail(url= user.avatar_url) # Устанавливаем картинку сбоку ( В душе хз как назвать xD )

    await ctx.send(embed=emb)

@Bot.command() # Декоратор команды
async def info(ctx, userf: discord.Member = None): # Название команды и аргумент
    user = ctx.message.author if userf == None else userf # Проверка указан ли пользователь, если нет то заменяем автором команды
    status = user.status # Получаем статус

    if user.is_on_mobile() == True: stat = 'На телефоне' # Проверка статуса и указываем статус
    if status == discord.Status.online: stat = 'В сети' # Проверка статуса и указываем статус
    elif status == discord.Status.offline: stat = 'Не в сети' # Проверка статуса и указываем статус
    elif status == discord.Status.idle: stat = 'Не активен' # Проверка статуса и указываем статус
    elif status == discord.Status.dnd: stat = 'Не беспокоить' # Проверка статуса и указываем статус

    create_time = (datetime.datetime.today()-user.created_at).days # Узнаем кол-во дней в дискорде
    join_time = (datetime.datetime.today()-user.joined_at).days # Узнаем кол-во дней на сервере

    emb = discord.Embed(title='Профиль', colour= user.color) # Делаем ембед и устанавливаем цвет
    emb.add_field(name= 'Ник', value= user.display_name, inline= False) # Добавляем поле и заполняем 
    emb.add_field(name= 'ID', value= user.id, inline= False) # Добавляем поле и заполняем 
    
    if create_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни в дискорде
    else:
        emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( {create_time} {postfix(create_time, "день", "дня", "дней")})', inline= False)# Добавляем поле и заполняем кол-во дней в дискорде и подбираем окончание
    if join_time == 0: # Проверка на число дней
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни на сервере
    else:
        emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( {join_time} {postfix(join_time, "день", "дня", "дней")} )', inline= False) # Добавляем поле и заполняем кол-во дней на сервере и подбираем окончание
    emb.add_field(name= 'Наивысшая роль', value= f"<@&{user.top_role.id}>", inline= False) # Добавляем поле и заполняем роль
    emb.add_field(name= 'Статус', value= stat, inline= False) # Добавляем поле и заполняем статус
    emb.set_thumbnail(url= user.avatar_url) # Устанавливаем картинку сбоку ( В душе хз как назвать xD )

    await ctx.send(embed=emb)


@Bot.command() # Декоратор команды
async def ran_anime(ctx): # Название команды
    emb = discord.Embed(description= 'Вот подобраная аниме картинка.') # Переменная ембеда и его описание
    emb.set_image(url=nekos.img('avatar')) # Тут мы с помощью новой библиотеки ищем картинку на тему аватар и ставим её в ембед
    await ctx.send(embed=emb)  # Отпрвака ембеда 

@Bot.command() # Декоратор команды
async def ran_color(ctx): # Название команды
    clr = (random.randint(0,16777215)) # Генерируем рандомное число от 0 до 16777215, это нужно чтобы сделать цвет
    emb = discord.Embed( # Переменная ембеда
        description= f'Сгенерированый цвет : ``#{hex(clr)[2:]}``', # Jписание ембеда, и код с помощью которого мы делаем цвет
        colour= clr # Устанавливаем цвет ембеду
    )

    await ctx.send(embed=emb) # Отпрвака ембеда 

@Bot.command() # Декоратор команды
async def hello( ctx ):
    author = ctx.message.author

    await ctx.send( f' { author.mention } Привет, меня зовут **X_i_l_y_a_BOT**' )

@Bot.command() # Декоратор команды
async def creator( ctx ):
    author = ctx.message.author

    await ctx.send( f' { author.mention } Создатель бота https://www.youtube.com/channel/UCmPs7q403B4ePx9NLJkp7ag' )

@Bot.command() # Декоратор команды
async def owner( ctx ):
    author = ctx.message.author

    await ctx.send( f' { author.mention } Создатель сервера https://www.youtube.com/channel/UCFAqRwQvlaj29SMZq1gBGsg' )

@Bot.command() # Декоратор команды
async def help(ctx, member : discord.Member = None): # Название команды и аргументы
    user = ctx.message.author if member == None else member # Проверка аргуменат и переменная участника
    emb = discord.Embed( # Переменная ембеда
        title=f'Команды', # Заполняем заголовок
        description= f'1. **owner** - можно узнать кто Создатель сервера\n2. **creator** - можно узнать кто Создатель бота\n3. **hello** - можно сказать привет боту\n4. **ran_color** - бот генерирует рандомный цвет в стиле HEX\n5. **ran_anime** - бот кидает рандомную аниме аватаркут\n6. **info** или **profile** - можно просмотреть информацию про участника\n7. **avatar** - можно увидеть аватар пользователя в высоком разришении', # Запонлняем описание
        color=user.color # Устанавливаем цвет
    )
    await ctx.send(embed=emb) # Отпрвака ембеда

@Bot.command() # Декоратор команды
async def ran_дибил( ctx ):
    author = ctx.message.author

    await ctx.send( f' { author.mention } https://avatars.mds.yandex.net/get-zen_doc/167204/pub_5d7c0a1598fe7900ad7282ea_5d7c0a1e8600e100add913c0/scale_1200' )

@Bot.command() # Декоратор команды
async def bstatus( ctx ):
    author = ctx.message.author

    await ctx.send( f' { author.mention } **бот успешно работает**. **Ошибок** **-** 0  ' )    

token = os.environ.get('BOT_TOKEN')
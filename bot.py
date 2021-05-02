import sched
import time
import asyncio
import threading

import config
import discord

config = config.get_config()

client = discord.Client()
s = sched.scheduler(time.time, time.sleep)
TOKEN = config['token']
RED_CARD: str = b"\xF0\x9F\x9F\xA5".decode("utf-8")
YELLOW_CARD: str = b"\xF0\x9F\x9F\xA8".decode("utf-8")
TIMEOUT_TIME: int = 120
loop = asyncio.get_event_loop()

timeouted = {}

def init():
    loop.create_task(client.start(TOKEN))
    threading.Thread(target=loop.run_forever())

def remove_timeout(user, role):
    asyncio.ensure_future(user.remove_roles(role), loop=loop)
    timeouted.pop(user.name, None)

async def add_timeout(user):
    timeouted[user.name] = True
    role = discord.utils.get(user.guild.roles, name="TIMEOUT")
    await user.add_roles(role)
    loop.call_later(TIMEOUT_TIME, lambda: remove_timeout(user, role))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == RED_CARD:
        red_card_count: int = next(filter(lambda x: x.emoji == RED_CARD, reaction.message.reactions)).count
        if red_card_count >= 3:
            if not timeouted.get(reaction.message.author.name, False):
                await add_timeout(reaction.message.author)
                await reaction.message.channel.send(f'{reaction.message.author} al lobby pete')
                await reaction.message.delete()
        print('TARJETA ROJA')

    if reaction.emoji == YELLOW_CARD:
        yellow_card_count: int = next(filter(lambda x: x.emoji == YELLOW_CARD, reaction.message.reactions)).count
        if yellow_card_count >= 3:
            if not timeouted.get(reaction.message.author.name, False):
                await add_timeout(reaction.message.author)
                await reaction.message.channel.send(f'{reaction.message.author} a tomar un poquito de aire')
        print('TARJETA AMARILLA')

init()

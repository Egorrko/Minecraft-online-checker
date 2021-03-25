import discord
from server import Server
from settings import Ds

client = discord.Client()
CHANNEL = None
ids = {}


def start_ds():
    client.run(Ds.TOKEN)


@client.event
async def on_ready():
    global CHANNEL
    CHANNEL = client.get_channel(Ds.CHANNEL_ID)


async def send(server: Server):
    try:
        if server.ip in ids:
            await ids[server.ip].edit(content=f'{server.text}\n.')
        else:
            msg = await CHANNEL.send(f'{server.text}\n.')
            ids[server.ip] = msg
    except Exception:
        pass

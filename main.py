import asyncio
import ds
import tg
from jsonw.reader import read
from settings import Tg, DELAY

servers = []


async def heartbeat(delay=DELAY):
    while True:
        await asyncio.sleep(delay)
        for server in servers:
            await server.update()
            await ds.send(server)
            await tg.send(server)
            if not server.online and Tg.ADMIN_ID != '':
                await tg.notify(server)


if __name__ == '__main__':
    read(servers)
    loop = asyncio.get_event_loop()
    loop.create_task(ds.start_ds())
    loop.create_task(heartbeat())
    loop.run_forever()

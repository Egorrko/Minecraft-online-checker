import json
from typing import List
from server import Server, MinecraftServer

def read(servers: List[Server]):
    with open('jsonw/servers.json', encoding='utf-8') as f:
        raw = json.loads(f.read())
        for i in raw:
            try:
                lookup = MinecraftServer.lookup(i['ip'])
                servers.append(Server(i['ip'], i['name'], lookup))
            except Exception:
                raise Exception(f'{i} is offline')

import json
import logging
from pathlib import Path
from contextlib import contextmanager

from pydantic import BaseModel, ValidationError
from app.config import config
from app.exceptions import ServersFileException


class ServerModel(BaseModel):
    address: str
    name: str

class ServersModel(BaseModel):
    servers: list[ServerModel] = []


def parser(text: str) -> ServersModel:
    if not text:
        return ServersModel()
    try:
        return ServersModel.parse_raw(text)
    except ValidationError:
        logging.error(f'Some error in your {config.SERVERS_FILE} file.')
        exit(1)


@contextmanager
def servers_file_opener():
    servers_file = Path(config.SERVERS_FILE)
    if not servers_file.exists():
        servers_file.touch()
    with servers_file.open("r+", encoding='utf-8') as f:
        servers = parser(f.read())
        yield (f, servers)
        f.truncate(0)
        f.seek(0)
        f.write(servers.json())


def add(address, name):
    servers_file = Path(config.SERVERS_FILE)
    if not servers_file.exists():
        servers_file.touch()
    with servers_file.open("r+", encoding='utf-8') as f:
        servers = parser(f.read())
        if any(serv.address == address for serv in servers.servers):
            logging.warning(f'This server already exists.')
            exit(0)
        servers = ServersModel(
                servers=servers.servers + [ServerModel(address=address, name=name)]
            )
        
        f.truncate(0)
        f.seek(0)
        f.write(servers.json())


def delete(address):
    with servers_file_opener() as servers:
        servers = ServersModel(
            servers=[serv for serv in servers.servers if serv.address != address]
        )
        print(servers)

def read():
    servers = []
    with open('servers.json', encoding='utf-8') as f:
        raw = [ServerModel.parse_obj(server) for server in json.loads(f.read())]
        for i in raw:
            lookup = None
            try:
                lookup = MinecraftServer.lookup(i['ip'])
            except Exception:
                logging.warning(f'{i} is offline')
            servers.append(Server(i['ip'], i['name'], lookup))

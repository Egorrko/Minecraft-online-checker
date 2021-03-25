import json

class Server:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name


servers = [Server('play.kopach.tk', 'Копач').__dict__,
           Server('play.kopach.tk:24545', 'Зипач').__dict__]

a = json.dumps(servers)

with open('servers.json', 'w', encoding='utf-8') as f:
    f.write(a)

print(a)
import time

from mcstatus import MinecraftServer


class Server:
    def __init__(self, ip: str, name: str, server: MinecraftServer):
        self.ip = ip
        self.name = name
        self.server = server
        self.online = True
        self.time = int(time.time())
        self.players = []
        self.ping = 0
        self.text = '.'

    def switch(self):
        self.online = not self.online
        self.time = int(time.time())

    async def update(self):
        try:
            status = await self.server.async_status()
            if status.players.sample is not None:
                self.players = sorted([player.name for player in status.players.sample])
            else:
                self.players = []
            self.ping = int(status.latency)
            if not self.online:
                self.switch()
        except Exception:
            if self.online:
                self.switch()
        self.prepare()

    def prepare(self):
        self.text = f'{self.ip}, {self.name}\n'
        if self.online:
            self.text += f'🟢 онлайн уже {self.bf_time()}\n' \
                         f'Пинг: {self.ping}\n' \
                         f'Игроков: {len(self.players)}\n' \
                         f'{self.bf_players()}'
        else:
            self.text += f'🔴 оффлайн уже {self.bf_time()}'

    def bf_players(self):
        result = ''
        for i in self.players:
            result += f'   {i}\n'
        return result

    def bf_time(self):
        diff = int(time.time()) - self.time
        return f'{diff // 3600}ч {diff % 3600 // 60}м {diff % 60}с'

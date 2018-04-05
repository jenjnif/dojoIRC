import socket

import bot


class Message:
    def __init__(self, prefix, command, *params):
        self.prefix = prefix
        self.command = command
        self.params = params

    @classmethod
    def parse(klass, line):
        if line[0] == ":":
            prefix, line = line.split(" ", 1)
        else:
            prefix = None
        command, line = line.split(" ", 1)
        params = []
        while line:
            if line[0] == ":" or " " not in line:
                params.append(line[1:])
                break
            param, line = line.split(" ", 1)
            params.append(param)
        return klass(prefix, command, *params)

    def __str__(self):
        parts = []
        if self.prefix:
            parts.append(self.prefix)
        parts.append(str(self.command))
        for param in self.params:
            if " " in param:
                parts.append(":" + param)
            else:
                parts.append(param)
        return " ".join(parts)


class Irc:
    def __init__(self, hostname, port, nickname, username, real_name, channel,
                 bot=None):
        self.hostname = hostname
        self.port = port
        self.nickname = nickname
        self.username = username
        self.real_name = real_name
        self.channel = channel
        self.bot = bot

    def connect(self):
        self.sock = socket.create_connection((self.hostname, self.port))
        self.conn = self.sock.makefile(mode='r', encoding='iso-8859-1')
        self.send(Message(None, "NICK", self.nickname))
        self.send(Message(None, "USER", self.username,
                          '0', "-", self.real_name))
        self.send(Message(None, "JOIN", self.channel))

    def send(self, message):
        self.sock.sendall(str(message).encode("iso-8859-1") + b"\r\n")

    def run(self):
        while True:
            line = self.conn.readline().strip()
            if not line:
                break
            msg = Message.parse(line)
            print(msg)
            if msg.command.isalpha():
                handler = getattr(self, "handle_" + msg.command.lower(), None)
                if handler:
                    handler(msg)

    def handle_ping(self, msg):
        self.send(Message(None, "PONG", msg.params))

    def handle_privmsg(self, msg):
        print("Received {!r} from {!r}".format(msg.params[1], msg.params[0]))
        if self.bot:
            reply = self.bot.public("", msg.params[0], msg.params[1])
            if reply:
                self.send(Message(None, "PRIVMSG", msg.params[0], reply))


if __name__ == '__main__':
    irc = Irc('irc.freenode.org', 6667, 'team2bot', 'team2bot',
              'London Python Dojo Team 2 Bot', '#pydojo', bot.Bot())
    irc.connect()
    irc.run()

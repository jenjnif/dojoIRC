import socket


class Message:
    def __init__(self, prefix, command, *params):
        self.prefix = prefix
        self.command = command
        self.params = params

    def __str__(self):
        if self.prefix:
            return ":{} {} {}".format(
                self.prefix, self.command, " ".join(self.params))
        return "{} {}".format(
            self.command, " ".join(self.params))


class Irc:
    def __init__(self, hostname, port, nickname, username, real_name):
        self.hostname = hostname
        self.port = port
        self.nickname = nickname
        self.username = username
        self.real_name = real_name

    def connect(self):
        self.sock = socket.create_connection((self.hostname, self.port))
        self.conn = self.sock.makefile(mode='r', encoding='iso-8859-1')
        self.send(Message(None, "NICK", self.nickname))
        self.send(Message(None, "USER", self.username,
                          '0', "-", self.real_name))

    def send(self, message):
        self.sock.sendall(str(message).encode("iso-8859-1") + b"\r\n")

    def run(self):
        while True:
            line = self.conn.readline().strip()
            if not line:
                break
            if line[0] == ":":
                msg = Message(*line.split(" "))
            else:
                msg = Message(None, *line.split(" "))
            print(msg)


if __name__ == '__main__':
    irc = Irc('irc.freenode.org', 6667, 'team2bot', 'team2bot',
              'London Python Dojo Team 2 Bot')
    irc.connect()
    irc.run()

class IRCInterface:
    def __init__(self, ircSocket):
        self.irc = ircSocket
        self.ircBuffer = ""

    def read(self):
        self.ircBuffer += self.irc.recv(4096)

        lastRF = self.ircBuffer.rfind("\r\n")
        if lastRF < 0:
            return []

        goodData = self.ircBuffer[:lastRF]
        self.ircBuffer = self.ircBuffer[lastRF+2:]

        for line in goodData.split("\r\n"):
            print "<= " + line

        return self.parseData(goodData)

    def send(self, data):
        print "=> " + data
        self.irc.send(data + "\r\n")

    def nick(self, nick):
        self.send('NICK %s' % nick)

    def user(self, username, hostname, servername, realname):
        self.send('USER %s %s %s :%s' % (username, hostname, servername, realname))

    def join(self, channel):
        self.send('JOIN %s' % channel)

    def pong(self, target):
        self.send('PONG :%s' % target)

    def privmsg(self, channel, text):
        self.send('PRIVMSG %s :%s' % (channel, text))

    def parseData(self, data):
        return map(self.parseMessage, data.split("\r\n"))

    def parseMessage(self, string):
        result = {}

        if string.find(':') == 0:
            split = string.split(' ', 1)
            result['prefix'] = split[0]
            string = split[1]

        colonindex = string.find(':')
        split = []
        if colonindex >= 0:
            split = string.split(' ', string[:colonindex].count(' '))
            split[-1] = split[-1][1:]
        else:
            split = string.split(' ')

        result['command'] = split[0]
        result['params'] = split[1:]

        return self.wrapMessage(result)

    def splitPrefix(self, prefix):
        prefix = prefix.split('!')
        prefix = [prefix[0][1:]] + prefix[1].split('@')
        return {"nick": prefix[0], "user": prefix[1], "host": prefix[2]}

    def wrapMessage(self, message):
        if message["command"] == "PRIVMSG":
            new = {"command": "PRIVMSG", "channel": message["params"][0], "text": message["params"][1]}
            new.update(self.splitPrefix(message["prefix"]))
            return new
        else:
            return message

import socket
import importlib
from ConfigLoader import ConfigLoader
from IRCInterface import IRCInterface
from EventDispatcher import EventDispatcher
from pprint import pprint
import inspect

class IRCBot:
    def __init__(self, configname):
        self.config = ConfigLoader(configname)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc = IRCInterface(self.socket)
        self.plugins = {}
        self.dispatcher = EventDispatcher(self.irc)

    def rise(self):
        self.loadAllPlugins()
        self.connect()

    def loadPlugin(self, pluginName):
        plugin = importlib.import_module("plugins." + pluginName)

        for name in dir(plugin):
            local = getattr(plugin, name)
            if hasattr(local, "_ircEvent"):
                self.dispatcher.hookEvent(getattr(local, "_ircEvent"), local)

    def loadAllPlugins(self):
        for m in self.config.get("plugins"):
            self.loadPlugin(m)

    def connect(self):
        self.socket.connect( (self.config.get("server"), int(self.config.get("port"))) )
        self.handshake()
        self.loop()

    def handshake(self):
        self.irc.nick(self.config.get("nick"))
        self.irc.user(self.config.get("nick"), "...", "...", "...")
        for channel in self.config.get("channels"):
            self.irc.join(channel)

    def loop(self):
        buffer = ""
        while True:
            data = self.irc.read()

            for cmd in data:
                if cmd["command"] == "PING":
                    self.irc.pong(cmd["params"][0])

                self.dispatcher.dispatch(cmd)

bot = IRCBot("config/connection.cfg")
bot.rise()

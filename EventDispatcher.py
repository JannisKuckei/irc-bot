class EventDispatcher:
    def __init__(self, irc):
        self.hooks = {}
        self.irc = irc

    def dispatch(self, msg):
        if msg["command"] in self.hooks:
            for func in self.hooks[msg["command"]]:
                try:
                    func(self.irc, msg)
                except KeyboardInterrupt:
                    raise
                except Exception as ex:
                    print "## %s->%s raised %s: '%s'" % (func.__module__, func.__name__, ex.__class__.__name__, ex)

    def hookEvent(self, command, func):
        if not command in self.hooks:
            self.hooks[command] = []
        self.hooks[command].append(func)

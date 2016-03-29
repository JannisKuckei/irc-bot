import hooks
import datetime

@hooks.event("PRIVMSG")
def timeCommand(irc, msg):
    if msg["text"] == ".time":
        irc.privmsg(msg["channel"], "%s: %s" % (msg["nick"], datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')))

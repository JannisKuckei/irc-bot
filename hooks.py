def event(eventname):
    def wrapper(func):
        func._ircEvent = eventname
        return func
    return wrapper

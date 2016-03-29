class ConfigLoader:
    def __init__(self, filename):
        cfgfile = open(filename, 'r')
        lines = filter(lambda x:  x != '' and x[0] != '#', cfgfile.read().split("\n"))

        self.cfg = {(j[0][1:] if j[0][0] == '*' else j[0]) : (j[1].split(' ') if j[0][0] == '*' else j[1]) for j in map(lambda x: x.split('='), lines)}

    def get(self, property):
        return self.cfg[property]

import cPickle


class Patent:

    def serialize(self, filename):
        f = file(filename, 'wb')
        cPickle.dump(self, f, protocol=cPickle.HIGHEST_PROTOCOL)
        f.close()


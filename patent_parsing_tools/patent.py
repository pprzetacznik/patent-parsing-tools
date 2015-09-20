# -*- coding: utf-8 -*-
#!/usr/bin/env python

import cPickle


class Patent:
    def serialize(self, filename):
        f = file(filename, 'wb')
        cPickle.dump(self, f, protocol=cPickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def load(source):
        """
        >>> patent = Patent()
        >>> patent.data = "test data"
        >>> patent.serialize("./serialized_patent")
        >>> patent2 = Patent.load("./serialized_patent")
        >>> print patent2.data
        test data
        """

        return cPickle.load(open(source, "rb"))


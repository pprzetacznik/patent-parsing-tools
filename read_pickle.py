import sys
import cPickle

__author__ = 'vreal'


if __name__ == '__main__':
    pikle_name = sys.argv[1]
    a = cPickle.load(open(pikle_name, "rb"))
    if len(sys.argv) == 2:
        print a
    elif len(sys.argv) == 3:
        string_length = int(sys.argv[2])
        print str(a)[0:string_length]
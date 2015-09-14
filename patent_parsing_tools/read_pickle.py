import sys
import cPickle
from patent import Patent

__author__ = 'vreal'


if __name__ == '__main__':
    pikle_name = sys.argv[1]
    a = cPickle.load(open(pikle_name, "rb"))

    if isinstance(a, list):
        p = a[0]
        if isinstance(p, Patent):
            for patent in a:
                print patent.title
                print patent.classification
    else :
        if len(sys.argv) == 2:
            print str(a)
        elif len(sys.argv) == 3:
            string_length = int(sys.argv[2])
            print str(a)[0:string_length]
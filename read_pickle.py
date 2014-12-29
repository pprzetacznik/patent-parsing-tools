import sys
import cPickle

__author__ = 'vreal'


if __name__ == '__main__':
    pikle_name = "/home/vreal/deepLearning/test_set/docs/xml_tuple_1"
    patent_list = cPickle.load(open(pikle_name, "rb"))
    if len(sys.argv) == 2:
        for patent in patent_list:
            print patent
    elif len(sys.argv) == 3:
        num_patents = int(sys.argv[2])
        for patent in patent_list:
            print patent
            num_patents -= 1
            if num_patents < 0:
                break

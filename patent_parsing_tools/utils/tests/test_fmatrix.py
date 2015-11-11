# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
import cPickle
import patent_parsing_tools.utils.fmatrix as fmatrix
import numpy as np
from pkg_resources import resource_filename


class TestFMatrix(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip("")
    def test_parse2(self):
        [did, matrix] = fmatrix.parse2('tests/train', 'tests/train.lex')
        print did
        self.assertIsNotNone(did)
        self.assertEqual(did[0], 1)
        self.assertEqual(did[1], 2)
        self.assertEqual(did[2], 3)
        self.assertEqual(did[3], 4)

    @unittest.skip("")
    def test_get_file_lines(self):
        self.assertEqual(fmatrix.get_file_lines('tests/train.lex'), 1324)

    def test_get_theano_dataset(self):
        trainset_filename = resource_filename("patent_parsing_tools.utils.tests", "train.txt")
        dictionary_filename = resource_filename("patent_parsing_tools.utils.tests", "dictionary.txt")
        train_set_x = fmatrix.get_theano_dataset(trainset_filename, dictionary_filename)
        self.assertEqual(train_set_x.get_value(borrow=True).shape, (10000, 10000))

    @unittest.skip("")
    def test_load_patents_dataset(self):
        dataset = fmatrix.load_patents_dataset('test/test_set')
        print dataset['08714876']
        print len(dataset['08714876'][0])
        print len(dataset)

        dataset2 = {}
        i = 0
        for k in dataset.keys():
            if i < 100:
                dataset2[k] = [dataset[k][0][:25], np.random.choice(['abc', 'def', 'gh'], 2).tolist()]
                i += 1
            else:
                break

        with open('test_vector2.pic', 'wb') as file:
            cPickle.dump(dataset2, file, cPickle.HIGHEST_PROTOCOL)

    def test_load_patents_dataset2(self):
        test_set_dir = resource_filename("patent_parsing_tools.utils.tests", "test_set")
        dataset = fmatrix.load_patents_dataset(test_set_dir)
        print dataset['08714876']
        print len(dataset['08714876'][0])
        print len(dataset)

    def test_get_test_set_with_categories(self):
        test_set_dir = resource_filename("patent_parsing_tools.utils.tests", "test_set")
        [_, matrix, _] = fmatrix.get_test_set_with_categories(test_set_dir)
        self.assertEqual(matrix.shape[0], 100)

    def test_concat_categories(self):
        categories_list = ['a', '44', 'F', '54']
        self.assertEqual(fmatrix.concat([], ['a']), ['a'])
        self.assertEqual(fmatrix.concat(['a'], []), ['a'])
        self.assertEqual(fmatrix.concat(['a'], ['44']), ['a', 'a44'])
        self.assertEqual(fmatrix.concat([], categories_list)[0], 'a')
        self.assertEqual(fmatrix.concat([], categories_list), ['a', 'a44', 'a44F', 'a44F54'])

    def test_parse_categories(self):
        categories_list = [['a', '44', 'F', '54'], ['b', '11', 'Z', '53']]
        self.assertEqual(fmatrix.parse_categories(categories_list, 0), ['a', 'b'])
        self.assertEqual(fmatrix.parse_categories(categories_list, 1), ['a44', 'b11'])

    def test_count_each_category(self):
        test_set_dir = resource_filename("patent_parsing_tools.utils.tests", "test_set")
        [_, _, categories] = fmatrix.get_test_set_with_categories(test_set_dir)
        cats = {}
        print len(categories)
        for i in categories:
            for j in categories[i]:
                if j in cats:
                    cats[j] += 1
                else:
                    cats[j] = 1
        for i in cats.keys():
            print "category['" + i + "'] = " + str(cats[i])

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

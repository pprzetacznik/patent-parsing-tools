from functools import reduce
import pickle
from os import listdir, path
import numpy as np
import theano


def get_file_lines(filename):
    with open(filename, "r") as fh:
        return sum(1 for _ in fh)


def parse2(filename, dictionary):
    """
    build a numpy full matrix from sparse 'id:cnt' data.
    """
    dictionary_size = get_file_lines(dictionary)
    file_lines = get_file_lines(filename)
    d = 0
    matrix = np.zeros((file_lines, dictionary_size))
    did = np.zeros(file_lines)
    with open(filename, "r") as fh:
        for line in fh:
            tokens = line.split()
            if len(tokens) > 0:
                did[d] = tokens[0]
                for token in tokens[1:]:
                    [id, cnt] = token.split(":")
                    v = int(id) - 1
                    c = float(cnt)
                    matrix[d, v] = c
                d += 1
    return [did, matrix]


def parse(filename, dictionary):
    """
    take only matrix from those two values returned from parse2(...) method
    """
    [did, matrix] = parse2(filename, dictionary)
    return matrix


def get_theano_dataset(filename, dictionary):
    X = parse(filename, dictionary)
    shared_x = theano.shared(np.asarray(X, dtype=theano.config.floatX))
    return shared_x


def load_patents_dataset(directory):
    print(f"loading {directory} dataset...")
    dataset = []
    files = [
        f for f in listdir(directory) if path.isfile(path.join(directory, f))
    ]
    for file in files:
        batch = load_patents_file(path.join(directory, file))
        dataset = dict(dataset, **batch)
    patents = len(dataset.keys())
    print(f"dataset {directory} loaded ({patents} patents)")
    return dataset


def load_patents_file(filepath):
    print(f"loading {filepath} batch...")
    with open(filepath, "rb") as f:
        try:
            data_set = pickle.load(f, encoding="latin1")
            return data_set
        except Exception as e:
            print(f"   could not load file ({e})")
            return {}


def concat(item, next):
    if len(next) == 0:
        return item
    if len(item) >= 1:
        return concat(
            item + [(item[-1] + (next[0] if not None else "None"))], next[1:]
        )
    else:
        return concat(item + [next[0]], next[1:])


def parse_categories(l, depth):
    reduce(lambda x, y: x + [concat([], y)[depth]], l, [])


def parse_categories(l, depth):
    return ["".join(categories[: depth + 1]) for categories in l]


def get_test_set_with_categories(directory, depth=0):
    data_set = load_patents_dataset(directory=directory)
    did = []
    matrix = []
    categories = {}
    for k in data_set.keys():
        did.append(k)
        matrix.append(data_set[k][0])
        categories[k] = parse_categories(data_set[k][1], depth)
    return [did, np.array(matrix, dtype=theano.config.floatX), categories]

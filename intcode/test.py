from os.path import dirname
from os.path import join


def resource_string(name):
    repo_root = dirname(dirname(__file__))
    p = join(repo_root, 'tests', 'resources', name)
    with open(p, 'r') as f:
        return f.read()


def load_memory(fname):
    input_ = resource_string(fname)
    return list(map(int, input_.strip().split(',')))


def load_int(fname):
    input_ = resource_string(fname)
    return int(input_.strip())

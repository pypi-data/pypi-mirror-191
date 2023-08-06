import pickle
import os

from .filelock import FileLock

PICKLE_PROTOCOL = 4


def load(file, **kwargs):
    #kwargs.setdefault('protocol', PICKLE_PROTOCOL)
    return pickle.load(file, **kwargs)


def dump(obj, file, **kwargs):
    kwargs.setdefault('protocol', PICKLE_PROTOCOL)
    return pickle.dump(obj, file, **kwargs)

def to_pickle(obj, filepath, **kwargs):
    with open(filepath, 'wb') as fout:
        dump(obj, fout, **kwargs)
    
def read_pickle(filepath, **kwargs):
    with open(filepath, 'rb') as fin:
        return load(fin, **kwargs)



def make_dir_if_necessary(dirname, max_depth=3):
    if os.path.isdir(dirname):
        return
    assert max_depth >= 0, "Cannot make too many nested directories. Something could be wrong!"
    if not os.path.isdir(os.path.dirname(dirname)):
        make_dir_if_necessary(os.path.dirname(dirname), max_depth - 1)
    fl = FileLock(dirname)
    with fl:
        print(f"{dirname} does not exist. Creating it for persist_to_disk")
        os.makedirs(dirname)
    return

def retrieve_id(meta_file, key, sep='||'):
    with FileLock(meta_file):
        curr_dict, lines = dict(), []
        if os.path.isfile(meta_file):
            with open(meta_file, 'r') as fin:
                lines = fin.readlines()
                curr_dict = dict([line.strip().split(sep) for line in lines])
        if key not in curr_dict:
            curr_dict[key] = pid = str(len(curr_dict)+1)
            with open(meta_file, 'a') as fout:
                fout.write(f"{key}{sep}{pid}\n")
    return curr_dict[key]

        
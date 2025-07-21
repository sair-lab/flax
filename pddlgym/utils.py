"""Utilities
"""
from collections import defaultdict
import contextlib
import sys
import itertools


def get_object_combinations(objects, arity, var_types=None, 
                            type_to_parent_types=None, allow_duplicates=False):
    type_to_objs = defaultdict(list)

    for obj in sorted(objects):
        if type_to_parent_types is None:
            type_to_objs[obj.var_type].append(obj)
        else:
            for t in type_to_parent_types[obj.var_type]:
                type_to_objs[t].append(obj)

    if var_types is None:
        choices = [sorted(objects) for _ in range(arity)]
    else:
        assert len(var_types) == arity
        choices = [type_to_objs[vt] for vt in var_types]

    for choice in itertools.product(*choices):
        if not allow_duplicates and len(set(choice)) != len(choice):
            continue
        yield choice

class DummyFile:
    def write(self, x):
        pass

    def flush(self):
        pass

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout

import os


def main(*args, **kwargs):
    '''
    Generic entry point to run a node tree application using
    IMPORT and FROM environment variables to specify application path.
    '''
    name = os.environ['IMPORT']
    path = os.environ['FROM']
    module = getattr(__import__(path), name)
    root = getattr(module, name)
    root.__fit__(*args, **kwargs)
    return root.__run__(*args, **kwargs)

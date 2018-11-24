
class ArgfinderException(Exception):
    pass


def format_path(path):
    if not path:
        return path
    relpath = os.path.relpath(path)
    return relpath if not relpath.startswith('..') else path

import argparse
import re

__version__ = '1.0.0'
WITHOUT_ARGS_REGEX = re.compile(r'\S+\(\)')
WITH_ARGS_REGEX = re.compile(r'\S+\(\s*([^)]+?)\s*\)')


def _parse_args():

    usage = "%(prog)s [options] PATH"
    version = "argfinder {0}".format(__version__)
    parser = argparse.ArgumentParser(prog='argfinder', usage=usage)
    parser.add_argument(
        'paths', nargs='+', metavar='PATH',
        help='Paths may be Python files or directories. For each directory'
        ' Argfinder analyzes all contained *.py files.')

    parser.add_argument('--version', action='version', version=version)
    return parser.parse_args()


class Argfinder(object):
    '''Find unspesified arguments'''

    def __init__(self, filename=''):
        self.defined_funcs = {}
        self.executed_funcs = {}
        self.code = {}
        self.filename = filename

    def parse(self):
        self.code = self.upload_code()
        for key in self.code.keys():
            if re.search(WITHOUT_ARGS_REGEX, self.code[key]):
                print('{}: {}'.format(key, self.code[key].strip()))

        # wout = WITHOUT_ARGS_REGEX.findall(self.code)
        # wt = WITH_ARGS_REGEX.findall(self.code)
        # print(wout)
        # print(wt)

    def upload_code(self):
        code = {}
        with open(self.filename, 'r') as f:
            for i, l in enumerate(f.read().splitlines()):
                code[str(i+1)] = l
            return code

def main():
    args = _parse_args()
    for path in args.paths:
        argfinder = Argfinder(path)
        argfinder.parse()

main()

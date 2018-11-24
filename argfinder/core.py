import argparse
import re

__version__ = '1.0.0'

REGEX = {
    'without_args': re.compile(r'\S+\(\)'),
    'without_args_with_parents': re.compile(r'(\w+\.\w+)(?=\()'),
    'with_args': re.compile(r'\S+\(\s*([^)]+?)\s*\)'),
}
REGEX_LIST = '\ '.join(['{}'.format(v) for v in REGEX.values()]).replace(' ', '')

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
            value = self.code[key].strip()
            if REGEX['without_args'].search(value):
                if value[:3] == 'def':
                    self.defined_funcs[value[3:].split('(')[0]] = {'required': [], 'optional': [], 'parent': None}
                else:
                    with_parent = REGEX['without_args_with_parents'].findall(value)
                    if with_parent:
                        for v in with_parent:
                            if v not in REGEX_LIST:
                                print(with_parent)
                    # print('{}: {} ---- EXEC func'.format(key, value))
        print(self.defined_funcs)


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

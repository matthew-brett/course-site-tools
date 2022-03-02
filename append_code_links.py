#!/usr/bin/env python
""" Append code links directive to pages with nbplots
"""

import re
from argparse import ArgumentParser, RawDescriptionHelpFormatter


NBPLOTS_RE = re.compile(r'^..\s+nbplot::', re.M)


def append_code_links(fname, dry_run=True):
    with open(fname, 'rt') as fobj:
        contents = fobj.read()
    if not NBPLOTS_RE.search(contents):
        if dry_run:
            print(f'No nbplots in {fname}')
        return
    if dry_run:
        # print(f'Will append code-links to {fname}')
        pass
    with open(fname, 'wt') as fobj:
        fobj.write(contents)
        fobj.write('\n\n.. code-links:: clear\n')


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('rst_file', nargs='+',
                        help='ReST file names')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    for fname in args.rst_file:
        append_code_links(fname)


if __name__ == '__main__':
    main()

""" Tests for proc_rst module

Run with::

    py.test test_proc_rst.py
"""

import sys
from os.path import dirname, join as pjoin
from glob import glob

import pytest

MY_DIR = dirname(__file__)
sys.path.append(dirname(__file__))

from proc_rst import process_doctest_block, process_rst, build_pages

EXAMPLE_DIR = pjoin(MY_DIR, 'examples')


def test_process_doctest_block():
    assert process_doctest_block(['']) == ''
    assert process_doctest_block(['>>> ']) == ''
    assert process_doctest_block(['>>> foo = 1']) == 'foo = 1'
    assert process_doctest_block(['>>> if foo == 1:\n',
                                  '...     bar = 2']) == (
                                      'if foo == 1:\n    bar = 2')


def test_process_solution():
    # Test processing of solution-start etc blocks
    template = """\
.. solution-start

    Text

.. solution-replace-code

    code

.. solution-end
"""
    soln, exercise, code, title, underline = process_rst(template)
    assert (soln, exercise, code, title, underline) == (
        '\n    Text\n\n', '', '\ncode\n\n', None, None)
    template = """\
.. solution-start

    Text

.. solution-replace

    Exercise

.. solution-end
"""
    soln, exercise, code, title, underline = process_rst(template)
    assert (soln, exercise, code, title, underline) == (
        '\n    Text\n\n', '\n    Exercise\n\n', '', None, None)
    template = """\
.. solution-start

    Text

.. solution-replace

    Exercise

"""
    with pytest.raises(ValueError):
        process_rst(template)
    template = """\
.. solution-start

    Text

.. solution-replace-code

    code

"""
    with pytest.raises(ValueError):
        process_rst(template)


class Args(object):
    exercise_code = None
    solution_page = None
    exercise_page = None
    new_title = None


def test_regression():
    # Test results from this run same as previous
    args = Args()
    for template in glob(pjoin(EXAMPLE_DIR, '*.tpl')):
        args.solution_fname = template
        pages = build_pages(args)
        assert sorted(pages) == ['code', 'exercise', 'solution']
        for out, contents in pages.values():
            with open(pjoin(EXAMPLE_DIR, out), 'rt') as fobj:
                assert fobj.read() == contents

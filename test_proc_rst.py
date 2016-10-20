""" Tests for proc_rst module

Run with::

    py.test test_proc_rst.py
"""

import sys
from os.path import dirname, basename, join as pjoin
from glob import glob

import pytest

MY_DIR = dirname(__file__)
sys.path.append(dirname(__file__))

from proc_rst import doctest2code, process_rst, build_pages

EXAMPLE_DIR = pjoin(MY_DIR, 'examples')
TPL_HIDDEN_SOLUTION = pjoin(EXAMPLE_DIR, 'on_dummies.tpl')


def test_doctest2code():
    assert doctest2code(['']) == ''
    assert doctest2code(['>>> ']) == ''
    assert doctest2code(['>>> foo = 1']) == 'foo = 1'
    assert doctest2code(['>>> if foo == 1:\n',
                         '...     bar = 2']) == (
                             'if foo == 1:\n    bar = 2')


def test_doctest_end():
    template = """\
Text

>>> a = 1
"""
    assert (process_rst(template) == (template, 'Text\n\n', '', None, None))
    template = """\
Text

>>> a = 1

More text
"""
    assert (process_rst(template) == (
        template, 'Text\n\n\nMore text\n', '', None, None))
    template = """\
>>> a = 1
"""
    assert (process_rst(template) == (
        template, '', '', None, None))
    template = """\
>>> #: preserve
>>> a = 1
"""
    assert (process_rst(template) == (
        template, template, '#: preserve\na = 1\n', None, None))
    template = """\
>>> #- comment only
>>> a = 1
"""
    assert (process_rst(template) == (
        template,
        ">>> #- comment only\n",
        '#- comment only\n', None, None))


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


def test_doctest_with_output():
    template = """\

.. nbplot::

    >>> #: doctest with output
    >>> print(1)
    1
    >>> print(2)
    2

"""
    soln, exercise, code, title, underline = process_rst(template)
    assert (soln, exercise, code, title, underline) == (
        template, template, """\
#: doctest with output
print(1)
print(2)
""",
        None, None)


class Args(object):
    exercise_code = None
    solution_page = None
    exercise_page = None
    new_title = None


def assert_as_before(pages):
    for out, contents in pages.values():
        with open(pjoin(EXAMPLE_DIR, out), 'rt') as fobj:
            original = fobj.read()
        assert original == contents


def test_regression():
    # Test results from this run same as previous build.
    # Edit the examples when fixing bugs in parser.
    args = Args()
    for template in glob(pjoin(EXAMPLE_DIR, '*.tpl')):
        if template == TPL_HIDDEN_SOLUTION:
            continue
        args.template_fname = template
        pages = build_pages(args)
        assert sorted(pages) == ['code', 'exercise', 'solution']
        assert_as_before(pages)
    # Test fussy page with no linked solution
    args.template_fname = TPL_HIDDEN_SOLUTION
    args.solution_page = ''
    pages = build_pages(args)
    assert sorted(pages) == ['code', 'exercise']
    assert_as_before(pages)
    args.solution_page = None
    args.exercise_page = ''
    args.exercise_code = ''
    pages = build_pages(args)
    assert sorted(pages) == ['solution']
    assert_as_before(pages)

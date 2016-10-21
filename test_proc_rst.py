""" Tests for proc_rst module

Run with::

    py.test test_proc_rst.py
"""

import sys
from os import getcwd
from os.path import dirname, join as pjoin
from glob import glob

import pytest

MY_DIR = dirname(__file__)
sys.path.append(dirname(__file__))

from proc_rst import doctest2code, process_rst, build_pages, process_title
from tmpdirs import dtemporize

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
    assert process_rst(template) == (template, 'Text\n\n', '', [])
    template = """\
Text

>>> a = 1

More text
"""
    assert (process_rst(template) == (
        template, 'Text\n\n\nMore text\n', '', []))
    template = """\
>>> a = 1
"""
    assert (process_rst(template) == (
        template, '', '', []))
    template = """\
>>> #: preserve
>>> a = 1
"""
    assert (process_rst(template) == (
        template, template, '#: preserve\na = 1\n', []))
    template = """\
>>> #- comment only
>>> a = 1
"""
    assert (process_rst(template) == (
        template,
        ">>> #- comment only\n",
        '#- comment only\n', []))


def assert_file_contents(fname, contents):
    with open(fname, 'rt') as fobj:
        file_contents = fobj.read()
    assert file_contents == contents


def assert_pages_as_files(pages, out_dir=None):
    out_dir = getcwd() if out_dir is None else out_dir
    for out, contents in pages.values():
        assert_file_contents(pjoin(out_dir, out), contents)


@dtemporize
def test_conditional_builds():
    # Test the conditional building works correctly
    template = """\
-----
Title
-----

Text

>>> #- comment
>>> a = 1

Text2
"""
    with open('a.tpl', 'wt') as fobj:
        fobj.write(template)
    args = Args()
    args.template_fname = 'a.tpl'
    pages = build_pages(args)
    expected_code = ('a_code.py', '""" Title\n"""\n#- comment\n')
    expected_solution = ('a_solution.rst', template)
    assert sorted(pages) == ['code', 'exercise', 'solution']
    assert pages['code'] == expected_code
    assert pages['solution'] == expected_solution
    assert pages['exercise'] == ('a_exercise.rst', """\
-----
Title
-----

* For code template see: :download:`a_code.py`;
* For solution see: :doc:`a_solution`.

Text

>>> #- comment

Text2
""")


def test_process_title():
    template = """\
-----
Title
-----

Text"""
    new_rst = process_title(template,
                            ['-----\n',
                             'Title\n',
                             '-----\n'], 'New title', 'foo')
    assert new_rst == ("""\
---------
New title
---------

foo
Text""")
    template = """\
-----
Title
-----

Text

>>> #- comment
>>> a = 1

Text2"""
    new_rst = process_title(template,
                            ['-----\n',
                             'Title\n',
                             '-----\n'], 'New title', 'foo')
    assert new_rst == ("""\
---------
New title
---------

foo
Text

>>> #- comment
>>> a = 1

Text2""")


def test_process_rst():
    # Test basic ReST parsing
    # Good title works OK
    template = """\
-----
Title
-----

Text"""
    for char in '=+#-':
        rst = template.replace('-', char)
        line = char * len('Title') + '\n'
        assert process_rst(rst) == (
            (rst, rst, '', [line, 'Title\n', line]))
    rst = template.replace('-----', '#####', 1)
    # Error from different overline and underline
    with pytest.raises(ValueError):
        process_rst(rst)
    # Remove line - now no title
    rst = rst.replace('#####', '', 1)
    with pytest.raises(ValueError):
        process_rst(rst)


def test_process_solution():
    # Test processing of solution-start etc blocks
    template = """\
.. solution-start

    Text

.. solution-replace-code

    code

.. solution-end
"""
    soln, exercise, code, t_lines = process_rst(template)
    assert (soln, exercise, code, t_lines) == (
        '\n    Text\n\n', '', '\ncode\n\n', [])
    template = """\
.. solution-start

    Text

.. solution-replace

    Exercise

.. solution-end
"""
    soln, exercise, code, t_lines = process_rst(template)
    assert (soln, exercise, code, t_lines) == (
        '\n    Text\n\n', '\n    Exercise\n\n', '', [])
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
    soln, exercise, code, t_lines = process_rst(template)
    assert (soln, exercise, code, t_lines) == (
        template, template, """\
#: doctest with output
print(1)
print(2)
""",
        [])


class Args(object):
    exercise_code = None
    solution_page = None
    exercise_page = None
    new_title = None


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
    # Test fussy page with no linked solution
    args.template_fname = TPL_HIDDEN_SOLUTION
    args.solution_page = ''
    pages = build_pages(args)
    assert sorted(pages) == ['code', 'exercise']
    assert_pages_as_files(pages, EXAMPLE_DIR)
    args.solution_page = None
    args.exercise_page = ''
    args.exercise_code = ''
    pages = build_pages(args)
    assert sorted(pages) == ['solution']
    assert_pages_as_files(pages, EXAMPLE_DIR)

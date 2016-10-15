""" Tests for proc_rst module

Run with::

    py.test test_proc_rst.py
"""

import sys
from os.path import dirname

import pytest

sys.path.append(dirname(__file__))

from proc_rst import process_doctest_block, process_rst


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

# Copyright 2009 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from __future__ import absolute_import, print_function, unicode_literals

__metaclass__ = type

import doctest
import os


DOCTEST_FLAGS = (
    doctest.ELLIPSIS |
    doctest.NORMALIZE_WHITESPACE |
    doctest.REPORT_NDIFF)


# The setUp() and tearDown() functions ensure that this doctest is not umask
# dependent.
def setUp(testobj):
    testobj._old_umask = os.umask(0o22)


def tearDown(testobj):
    os.umask(testobj._old_umask)


def load_tests(loader, tests, pattern):
    globs = {
        "absolute_import": absolute_import,
        "print_function": print_function,
        "unicode_literals": unicode_literals,
        }
    tests.addTest(doctest.DocFileSuite(
        "filesystem.txt", setUp=setUp, tearDown=tearDown, globs=globs,
        optionflags=DOCTEST_FLAGS))
    return tests

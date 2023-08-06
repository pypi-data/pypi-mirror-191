# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook_media.tests.test_line import LineTestCase


__all__ = ['suite']


class CashbookTestCase(\
    LineTestCase,
    ):
    'Test cashbook module'
    module = 'cashbook_media'

# end CashbookTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CashbookTestCase))
    return suite

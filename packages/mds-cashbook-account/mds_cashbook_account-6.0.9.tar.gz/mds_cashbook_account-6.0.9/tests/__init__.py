# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook_account.tests.test_category import CategoryTestCase
from trytond.modules.cashbook_account.tests.test_line import LineTestCase

__all__ = ['suite']


class CashbookAccountTestCase(\
    CategoryTestCase,\
    LineTestCase,\
    ):
    'Test cashbook account module'
    module = 'cashbook_account'

# end CashbookAccountTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CashbookAccountTestCase))
    return suite

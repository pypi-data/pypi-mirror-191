# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook_analytic.tests.test_analytic import AnalyticTestCase

__all__ = ['suite']


class CashbookAnalyticTestCase(\
    AnalyticTestCase,\
    ):
    'Test cashbook exchange module'
    module = 'cashbook_analytic'

# end CashbookAnalyticTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CashbookAnalyticTestCase))
    return suite

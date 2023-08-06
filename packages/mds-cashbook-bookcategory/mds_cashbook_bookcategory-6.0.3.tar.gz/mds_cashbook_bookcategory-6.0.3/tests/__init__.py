# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook_bookcategory.tests.test_category import CategoryTestCase


__all__ = ['suite']


class CashbookCategoryTestCase(\
    CategoryTestCase,\
    ):
    'Test cashbook module'
    module = 'cashbook_bookcategory'

# end CashbookCategoryTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CashbookCategoryTestCase))
    return suite

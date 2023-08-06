# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook_dataexchange.tests.test_category import CategoryTestCase
from trytond.modules.cashbook_dataexchange.tests.test_party import PartyTestCase
from trytond.modules.cashbook_dataexchange.tests.test_transaction import TransactionTestCase

__all__ = ['suite']


class CashbookExchangeTestCase(\
    CategoryTestCase,\
    PartyTestCase,\
    TransactionTestCase,\
    ):
    'Test cashbook exchange module'
    module = 'cashbook_dataexchange'

# end CashbookExchangeTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CashbookExchangeTestCase))
    return suite

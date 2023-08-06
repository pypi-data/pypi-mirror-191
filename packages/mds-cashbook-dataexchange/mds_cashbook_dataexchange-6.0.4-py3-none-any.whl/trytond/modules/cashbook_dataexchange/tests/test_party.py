# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from datetime import date
from decimal import Decimal
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from .qifdata import qif_types


class PartyTestCase(ModuleTestCase):
    'Test cashbook party module'
    module = 'cashbook_dataexchange'

    @with_transaction()
    def test_wiz_import_party(self):
        """ create parties by run wizard
        """
        pool = Pool()
        Party = pool.get('party.party')
        ImportWiz = pool.get('cashbook_dataexchange.qif_imp_wiz', type='wizard')

        company = self.prep_company()
        with Transaction().set_context({
            'company': company.id,
            'active_model': 'party.party',
            }):
            (sess_id, start_state, end_state) = ImportWiz.create()
            w_obj = ImportWiz(sess_id)
            self.assertEqual(start_state, 'start')
            self.assertEqual(end_state, 'end')

            # run start
            result = ImportWiz.execute(sess_id, {}, start_state)
            self.assertEqual(list(result.keys()), ['view'])
            self.assertEqual(result['view']['defaults']['company'], company.id)

            r1 = {}
            r1['file_'] = qif_types.encode('utf8')
            r1['company'] = company.id
            w_obj.start.file_ = r1['file_']
            w_obj.start.company = company.id

            result = ImportWiz.execute(sess_id, {'start': r1}, 'readf')

            self.assertEqual(list(result.keys()), ['view'])
            self.assertEqual(result['view']['defaults']['company'], company.id)
            self.assertEqual(result['view']['defaults']['info'],
"""The following 3 parties are now imported:\n
Opening Balance
GA NR00002168 BLZ10000000 0
Foodshop Zehlendorf""")

            r1 = {'company': company.id}
            result = ImportWiz.execute(sess_id, {'showinfo': r1}, 'importf')
            self.assertEqual(list(result.keys()), [])

            ImportWiz.delete(sess_id)

            records = Party.search([], order=[('name', 'ASC')])
            self.assertEqual(len(records), 4)

            self.assertEqual(records[0].rec_name, 'Foodshop Zehlendorf')
            self.assertEqual(records[1].rec_name, 'GA NR00002168 BLZ10000000 0')
            self.assertEqual(records[2].rec_name, 'm-ds')
            self.assertEqual(records[3].rec_name, 'Opening Balance')

# end PartyTestCase

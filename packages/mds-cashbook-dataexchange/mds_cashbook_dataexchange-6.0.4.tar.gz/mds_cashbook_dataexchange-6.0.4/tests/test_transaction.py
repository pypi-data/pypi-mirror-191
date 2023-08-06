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


class TransactionTestCase(ModuleTestCase):
    'Test cashbook transaction module'
    module = 'cashbook_dataexchange'

    @with_transaction()
    def test_func_check_counter_transaction(self):
        """ check function 'check_counter_transaction'
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        QifTool = pool.get('cashbook_dataexchange.qiftool')

        company = self.prep_company()
        with Transaction().set_context({
            'company': company.id,
            }):
            types = self.prep_type()
            books = Book.create([{
                'name': 'Cash Book',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2010, 1, 1),
                }, {
                'name': 'S-Giro',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2010, 1, 1),
                }])

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'date': date(2022, 6, 1),
                        'bookingtype':'mvout',
                        'amount': Decimal('10.0'),
                        'booktransf': books[1].id,
                        'description': 'transfer',
                        }])],
                }])
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(books[0].lines[0].rec_name,
                '06/01/2022|to|-10.00 usd|transfer [S-Giro | 0.00 usd | Open]')
            self.assertEqual(len(books[1].lines), 0)

            Line.wfcheck(books[0].lines)
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(books[1].lines[0].rec_name,
                '06/01/2022|from|10.00 usd|transfer [Cash Book | -10.00 usd | Open]')

            self.assertEqual(QifTool.check_counter_transaction(books[1], {
                    'booktransf': books[0].id,
                    'date': date(2022, 6, 1),
                    'amount': Decimal('10.0'),
                    'description': 'transfer',
                    'bookingtype': 'mvin',
                }), True)

    @with_transaction()
    def test_wiz_import_transactions(self):
        """ create transactions by run wizard
        """
        pool = Pool()
        Party = pool.get('party.party')
        Category = pool.get('cashbook.category')
        Book = pool.get('cashbook.book')
        ImportWiz = pool.get('cashbook_dataexchange.qif_imp_wiz', type='wizard')

        company = self.prep_company()
        with Transaction().set_context({
            'company': company.id,
            'active_model': 'cashbook.book',
            }):
            types = self.prep_type()
            books = Book.create([{
                'name': 'Cash Book',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2010, 1, 1),
                }, {
                'name': 'S-Giro',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2010, 1, 1),
                }, {
                'name': 'Bargeld',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2010, 1, 1),
                }])

            Party.create([{
                'name': 'GA NR00002168 BLZ10000000 0',
                'addresses':[('create', [{}])],
                }, {
                'name': 'Foodshop Zehlendorf',
                'addresses':[('create', [{}])],
                }, {
                'name': 'Opening Balance',
                'addresses':[('create', [{}])],
                }])

            Category.create([{
                    'name': 'Lebensmittel',
                    'cattype': 'out',
                }])

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
            r1['book'] = books[0].id
            w_obj.start.file_ = r1['file_']
            w_obj.start.company = company.id
            w_obj.start.book = books[0].id

            result = ImportWiz.execute(sess_id, {'start': r1}, 'readf')

            self.assertEqual(list(result.keys()), ['view'])
            self.assertEqual(result['view']['defaults']['company'], company.id)
            self.assertEqual(result['view']['defaults']['info'],
"""The following transactionen are now imported:
Credit: usd7.12
Debit: usd83.92
Balance: -usd76.80
Number of transactions: 4""")

            r1 = {
                'company': company.id,
                'book': books[0].id,
                }
            result = ImportWiz.execute(sess_id, {'showinfo': r1}, 'importf')
            self.assertEqual(list(result.keys()), [])

            ImportWiz.delete(sess_id)

            self.assertEqual(len(books[0].lines), 4)

            self.assertEqual(books[0].lines[0].rec_name, '12/04/2013|from|7.12 usd|Opening Balance [Bargeld | -7.12 usd | Open]')
            self.assertEqual(books[0].lines[1].rec_name, '12/05/2013|to|-29.00 usd|GA NR00002168 BLZ10000000 0; 05.12/06.42 [S-Giro | 29.00 usd | Open]')
            self.assertEqual(books[0].lines[2].rec_name, '12/05/2013|Exp|-56.37 usd|some food [Lebensmittel]')
            self.assertEqual(books[0].lines[3].rec_name, '12/06/2013|Exp|1.45 usd|return of bottles [Lebensmittel]')

            self.assertEqual(Book.export_as_qif(books[0]), """!Type:Bank
D12/04/2013
T7.12
CX
L[Bargeld]
MOpening Balance
^
D12/05/2013
T-29.00
CX
L[S-Giro]
MGA NR00002168 BLZ10000000 0; 05.12/06.42UHR TT TELTOW
^
D12/05/2013
T-56.37
CX
PFoodshop Zehlendorf
LLebensmittel
Msome food
^
D12/06/2013
T1.45
CX
PFoodshop Zehlendorf
LLebensmittel
Mreturn of bottles
^""")

    @with_transaction()
    def test_wiz_import_transactions_transfer(self):
        """ create transactions by run wizard,
            handle transfers
        """
        pool = Pool()
        Party = pool.get('party.party')
        Category = pool.get('cashbook.category')
        Book = pool.get('cashbook.book')
        ImportWiz = pool.get('cashbook_dataexchange.qif_imp_wiz', type='wizard')

        company = self.prep_company()
        with Transaction().set_context({
            'company': company.id,
            'active_model': 'cashbook.book',
            }):
            types = self.prep_type()
            books = Book.create([{
                'name': 'From Book',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2010, 1, 1),
                }, {
                'name': 'To Book',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2010, 1, 1),
                }])

            Party.create([{
                'name': 'Foodshop Zehlendorf',
                'addresses':[('create', [{}])],
                }])

            Category.create([{
                    'name': 'Lebensmittel',
                    'cattype': 'out',
                }, {
                    'name': 'Fee',
                    'cattype': 'out',
                }])

            (sess_id, start_state, end_state) = ImportWiz.create()
            w_obj = ImportWiz(sess_id)
            self.assertEqual(start_state, 'start')
            self.assertEqual(end_state, 'end')

            # run start
            result = ImportWiz.execute(sess_id, {}, start_state)
            self.assertEqual(list(result.keys()), ['view'])
            self.assertEqual(result['view']['defaults']['company'], company.id)

            r1 = {}
            r1['file_'] = """!Type:Bank
D05.12.2013
CX
Msome food
T-50,25
PFoodshop Zehlendorf
LLebensmittel
^
D04.12.2013
T-7,30
CX
PTransfer to book
L[To Book]
^""".encode('utf8')
            r1['company'] = company.id
            r1['book'] = books[0].id
            w_obj.start.file_ = r1['file_']
            w_obj.start.company = company.id
            w_obj.start.book = books[0].id

            result = ImportWiz.execute(sess_id, {'start': r1}, 'readf')

            self.assertEqual(list(result.keys()), ['view'])
            self.assertEqual(result['view']['defaults']['company'], company.id)
            self.assertEqual(result['view']['defaults']['info'],
"""The following transactionen are now imported:
Credit: usd0.00
Debit: usd57.55
Balance: -usd57.55
Number of transactions: 2""")

            r1 = {
                'company': company.id,
                'book': books[0].id,
                }
            result = ImportWiz.execute(sess_id, {'showinfo': r1}, 'importf')
            self.assertEqual(list(result.keys()), [])

            ImportWiz.delete(sess_id)

            self.assertEqual(len(books[0].lines), 2)
            self.assertEqual(len(books[1].lines), 1)

            self.assertEqual(books[0].lines[0].rec_name, '12/04/2013|to|-7.30 usd|Transfer to book [To Book | 7.30 usd | Open]')
            self.assertEqual(books[0].lines[0].state, 'check')
            self.assertEqual(books[0].lines[1].rec_name, '12/05/2013|Exp|-50.25 usd|some food [Lebensmittel]')
            self.assertEqual(books[0].lines[1].state, 'check')
            self.assertEqual(books[1].lines[0].rec_name, '12/04/2013|from|7.30 usd|Transfer to book [From Book | -57.55 usd | Open]')
            self.assertEqual(books[1].lines[0].state, 'check')

            # run wizard again - import to 'To Book'
            (sess_id, start_state, end_state) = ImportWiz.create()
            w_obj = ImportWiz(sess_id)
            self.assertEqual(start_state, 'start')
            self.assertEqual(end_state, 'end')

            # run start
            result = ImportWiz.execute(sess_id, {}, start_state)
            self.assertEqual(list(result.keys()), ['view'])
            self.assertEqual(result['view']['defaults']['company'], company.id)

            r1 = {}
            r1['file_'] = """!Type:Bank
D10.12.2013
CX
Msome food
T-10,00
PFoodshop Zehlendorf
LLebensmittel
^
D04.12.2013
T7,30
CX
PTransfer to book
L[From Book]
^
D06.12.2013
T-10,00
CX
PFoodshop Zehlendorf
MSplitbooking with category and account
LFee
SFee
EFee for transfer
$-3,00
S[From Book]
ETransfer to From-Book
$-7,00
^
""".encode('utf8')
            r1['company'] = company.id
            r1['book'] = books[1].id
            w_obj.start.file_ = r1['file_']
            w_obj.start.company = company.id
            w_obj.start.book = books[1].id

            result = ImportWiz.execute(sess_id, {'start': r1}, 'readf')

            self.assertEqual(list(result.keys()), ['view'])
            self.assertEqual(result['view']['defaults']['company'], company.id)
            self.assertEqual(result['view']['defaults']['info'],
"""The following transactionen are now imported:
Credit: usd0.00
Debit: usd20.00
Balance: -usd20.00
Number of transactions: 2""")

            r1 = {
                'company': company.id,
                'book': books[1].id,
                }
            result = ImportWiz.execute(sess_id, {'showinfo': r1}, 'importf')
            self.assertEqual(list(result.keys()), [])

            ImportWiz.delete(sess_id)

            self.assertEqual(len(books[0].lines), 3)
            self.assertEqual(len(books[1].lines), 3)

            self.assertEqual(books[0].lines[0].rec_name, '12/04/2013|to|-7.30 usd|Transfer to book [To Book | -12.70 usd | Open]')
            self.assertEqual(books[0].lines[0].state, 'check')
            self.assertEqual(books[0].lines[1].rec_name, '12/05/2013|Exp|-50.25 usd|some food [Lebensmittel]')
            self.assertEqual(books[0].lines[1].state, 'check')
            self.assertEqual(books[0].lines[2].rec_name, '12/06/2013|from|7.00 usd|Transfer to From-Book [To Book | -12.70 usd | Open]')
            self.assertEqual(books[0].lines[2].state, 'check')

            self.assertEqual(books[1].lines[0].rec_name, '12/04/2013|from|7.30 usd|Transfer to book [From Book | -50.55 usd | Open]')
            self.assertEqual(books[1].lines[0].state, 'check')
            self.assertEqual(books[1].lines[1].rec_name, '12/06/2013|Exp/Sp|-10.00 usd|Splitbooking with category and account [-]')
            self.assertEqual(books[1].lines[1].state, 'check')
            self.assertEqual(books[1].lines[2].rec_name, '12/10/2013|Exp|-10.00 usd|some food [Lebensmittel]')
            self.assertEqual(books[1].lines[2].state, 'check')

# end PartyTestCase

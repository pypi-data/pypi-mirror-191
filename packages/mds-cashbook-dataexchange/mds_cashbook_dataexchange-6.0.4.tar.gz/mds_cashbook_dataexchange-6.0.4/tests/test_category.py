# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from datetime import date
from decimal import Decimal
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.modules.cashbook.tests import CashbookTestCase
from .qifdata import qif_category, qif_types


class CategoryTestCase(CashbookTestCase):
    'Test cashbook categoy module'
    module = 'cashbook_dataexchange'

    @with_transaction()
    def test_wiz_import_category(self):
        """ create categories by run wizard
        """
        pool = Pool()
        Category = pool.get('cashbook.category')
        ImportWiz = pool.get('cashbook_dataexchange.qif_imp_wiz', type='wizard')

        company = self.prep_company()
        with Transaction().set_context({
            'company': company.id,
            'active_model': 'cashbook.category',
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
"""The following categories are now imported:\n
Gehalt (in)
Gehalt/Zulagen (in)

Telekommunikation (out)
Telekommunikation/Online-Dienste (out)
Telekommunikation/Telefon (out)
Telekommunikation/Telefon/Test1 (out)
Telekommunikation/Fernsehen (out)
Telefon (out)
Telefon/Telco1-Tablett (out)
Telefon/Telco2-Handy (out)
Telefon/Telco3 (out)
Fernsehen (out)
Fernsehen/TV-Company (out)
Fernsehen/GEZ (out)
Lebensmittel (out)""")

            r1 = {'company': company.id}
            result = ImportWiz.execute(sess_id, {'showinfo': r1}, 'importf')
            self.assertEqual(list(result.keys()), [])

            ImportWiz.delete(sess_id)

            records = Category.search([], order=[('rec_name', 'ASC')])
            self.assertEqual(len(records), 15)

            self.assertEqual(records[0].rec_name, 'Fernsehen')
            self.assertEqual(records[1].rec_name, 'Fernsehen/GEZ')
            self.assertEqual(records[2].rec_name, 'Fernsehen/TV-Company')
            self.assertEqual(records[3].rec_name,  'Gehalt')
            self.assertEqual(records[4].rec_name, 'Gehalt/Zulagen')
            self.assertEqual(records[5].rec_name, 'Lebensmittel')
            self.assertEqual(records[6].rec_name, 'Telefon')
            self.assertEqual(records[7].rec_name, 'Telefon/Telco1-Tablett')
            self.assertEqual(records[8].rec_name, 'Telefon/Telco2-Handy')
            self.assertEqual(records[9].rec_name, 'Telefon/Telco3')
            self.assertEqual(records[10].rec_name, 'Telekommunikation')
            self.assertEqual(records[11].rec_name, 'Telekommunikation/Fernsehen')
            self.assertEqual(records[12].rec_name, 'Telekommunikation/Online-Dienste')
            self.assertEqual(records[13].rec_name, 'Telekommunikation/Telefon')
            self.assertEqual(records[14].rec_name, 'Telekommunikation/Telefon/Test1')

    @with_transaction()
    def test_category_create_by_qif_emptydb(self):
        """ create categories by import a qif-file
        """
        pool = Pool()
        Category = pool.get('cashbook.category')

        company = self.prep_company()
        with Transaction().set_context({
            'company': company.id,
            }):
            records = Category.create_from_qif(qif_types)

            records = Category.search([], order=[('rec_name', 'ASC')])
            self.assertEqual(len(records), 15)

            self.assertEqual(records[0].rec_name, 'Fernsehen')
            self.assertEqual(records[1].rec_name, 'Fernsehen/GEZ')
            self.assertEqual(records[2].rec_name, 'Fernsehen/TV-Company')
            self.assertEqual(records[3].rec_name,  'Gehalt')
            self.assertEqual(records[4].rec_name, 'Gehalt/Zulagen')
            self.assertEqual(records[5].rec_name, 'Lebensmittel')
            self.assertEqual(records[6].rec_name, 'Telefon')
            self.assertEqual(records[7].rec_name, 'Telefon/Telco1-Tablett')
            self.assertEqual(records[8].rec_name, 'Telefon/Telco2-Handy')
            self.assertEqual(records[9].rec_name, 'Telefon/Telco3')
            self.assertEqual(records[10].rec_name, 'Telekommunikation')
            self.assertEqual(records[11].rec_name, 'Telekommunikation/Fernsehen')
            self.assertEqual(records[12].rec_name, 'Telekommunikation/Online-Dienste')
            self.assertEqual(records[13].rec_name, 'Telekommunikation/Telefon')
            self.assertEqual(records[14].rec_name, 'Telekommunikation/Telefon/Test1')

            result = Category.export_as_qif()
            self.assertEqual(result, """!Type:Cat
NFernsehen
E
^
NFernsehen:GEZ
E
^
NFernsehen:TV-Company
E
^
NLebensmittel
E
^
NTelefon
E
^
NTelefon:Telco1-Tablett
E
^
NTelefon:Telco2-Handy
E
^
NTelefon:Telco3
E
^
NTelekommunikation
E
^
NTelekommunikation:Fernsehen
E
^
NTelekommunikation:Online-Dienste
E
^
NTelekommunikation:Telefon
E
^
NTelekommunikation:Telefon:Test1
E
^
NGehalt
I
^
NGehalt:Zulagen
I
^""")

    @with_transaction()
    def test_category_create_by_qif_existing_categories(self):
        """ create categories by import a qif-file,
            some categories exists already
        """
        pool = Pool()
        Category = pool.get('cashbook.category')

        company = self.prep_company()
        with Transaction().set_context({
            'company': company.id,
            }):
            cat1, = Category.create([{
                'name': 'Telekommunikation',
                'cattype': 'out',
                'childs': [('create', [{
                    'cattype': 'out',
                    'name': 'Telefon',
                    }])],
                }])

            records = Category.search([])
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0].rec_name, 'Telekommunikation')
            self.assertEqual(records[1].rec_name, 'Telekommunikation/Telefon')

            records1 = Category.create_from_qif(qif_types)

            records = Category.search([], order=[('rec_name', 'ASC')])
            self.assertEqual(len(records), 15)

            self.assertEqual(records[0].rec_name, 'Fernsehen')
            self.assertEqual(records[1].rec_name, 'Fernsehen/GEZ')
            self.assertEqual(records[2].rec_name, 'Fernsehen/TV-Company')
            self.assertEqual(records[3].rec_name,  'Gehalt')
            self.assertEqual(records[4].rec_name, 'Gehalt/Zulagen')
            self.assertEqual(records[5].rec_name, 'Lebensmittel')
            self.assertEqual(records[6].rec_name, 'Telefon')
            self.assertEqual(records[7].rec_name, 'Telefon/Telco1-Tablett')
            self.assertEqual(records[8].rec_name, 'Telefon/Telco2-Handy')
            self.assertEqual(records[9].rec_name, 'Telefon/Telco3')
            self.assertEqual(records[10].rec_name, 'Telekommunikation')
            self.assertEqual(records[11].rec_name, 'Telekommunikation/Fernsehen')
            self.assertEqual(records[12].rec_name, 'Telekommunikation/Online-Dienste')
            self.assertEqual(records[13].rec_name, 'Telekommunikation/Telefon')
            self.assertEqual(records[14].rec_name, 'Telekommunikation/Telefon/Test1')

    @with_transaction()
    def test_qiftool_split_types(self):
        """ split file-content by types
        """
        QifTool = Pool().get('cashbook_dataexchange.qiftool')

        result = QifTool.split_by_type(qif_types)
        self.assertEqual(len(result.keys()), 2)
        self.assertEqual(result['Cat'], 'NGehalt\nI\n^\nNGehalt:Zulagen\n'+
            'I\n^\nNTelekommunikation\nE\n^\nNTelekommunikation:Online-Dienste\n'+
            'E\n^\nNTelekommunikation:Telefon\nE\n^\nNTelekommunikation:Telefon:Test1\n'+
            'E\n^\nNTelefon:Telco1-Tablett\n'+
            'E\n^\nNTelefon:Telco2-Handy\nE\n^\nNTelefon:Telco3\nE\n^\n'+
            'NTelekommunikation:Fernsehen\nE\n^\nNFernsehen:TV-Company\nE\n'+
            '^\nNFernsehen:GEZ\nE\n^\nNLebensmittel\nE\n^')
        self.assertEqual(result['Bank'], 'D04.12.2013\nT7,12\nCX\nPOpening Balance\n'+
            'L[Bargeld]\n^\nD05.12.2013\nCX\nM05.12/06.42UHR TT TELTOW\nT-29,00\n'+
            'PGA NR00002168 BLZ10000000 0\nL[S-Giro]\n^\nD05.12.2013\nCX\nMsome food\n'+
            'T-56,37\nPFoodshop Zehlendorf\nLLebensmittel\n^\nD06.12.2013\nCX\n'+
            'Mreturn of bottles\nT1,45\nPFoodshop Zehlendorf\nLLebensmittel\n^\n')

    @with_transaction()
    def test_qiftool_convert_transactions(self):
        """ convert_transactions_to_create
        """
        pool = Pool()
        QifTool = pool.get('cashbook_dataexchange.qiftool')
        Category = pool.get('cashbook.category')
        Party = pool.get('party.party')
        Book = pool.get('cashbook.book')

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
                }, {
                'name': 'Bargeld',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2010, 1, 1),
                }])
            self.assertEqual(books[0].name, 'Cash Book')
            self.assertEqual(books[1].name, 'S-Giro')
            self.assertEqual(books[2].name, 'Bargeld')
            self.assertEqual(books[0].btype.rec_name, 'CAS - Cash')
            self.assertEqual(books[1].btype.rec_name, 'CAS - Cash')
            self.assertEqual(books[2].btype.rec_name, 'CAS - Cash')

            parties = Party.create([{
                'name': 'Opening Balance',
                'addresses': [('create', [{}])],
                }, {
                'name': 'GA NR00002168 BLZ10000000 0',
                'addresses': [('create', [{}])],
                }, {
                'name': 'Foodshop Zehlendorf',
                'addresses': [('create', [{}])],
                }, {
                'name': 'real,- Teltow',
                'addresses': [('create', [{}])],
                }])

            categories = Category.create([{
                'name': 'Lebensmittel',
                'cattype': 'out',
                'company': company.id,
                }, {
                'name': 'Haushaltschemie',
                'cattype': 'out',
                'company': company.id,
                }, {
                'name': 'Kosmetik',
                'cattype': 'out',
                'company': company.id,
                }])

            tr_list = QifTool.qif_read_transactions('D04.12.2013\nT7,12\nCX\n'+
                'POpening Balance\nL[Bargeld]\n^\nD05.12.2013\nCX\n'+
                'M05.12/06.42UHR TT TELTOW\nT-29,00\nPGA NR00002168 BLZ10000000 0\n'+
                'L[S-Giro]\n^\nD05.12.2013\nCX\nMsome food\nT-56,37\n'+
                'PFoodshop Zehlendorf\nLLebensmittel\n^\nD22.10.2020\n'+
                'CX\nMLebensmittel\nT-55,84\nPreal,- Teltow\nLLebensmittel\n'+
                'SLebensmittel\nELebensmittel\n$-49,36\nSKosmetik\nEKlopapier\n'+
                '$-2,99\nSHaushaltschemie\nESagrotan\n$-3,49\n'+
                'S[S-Giro]\nEtransfer out\n$-3,49\n^\n')

            (to_create, msg_txt, fail_cnt) = QifTool.convert_transactions_to_create(books[0], tr_list)
            self.assertEqual(msg_txt, [])
            self.assertEqual(to_create, [{
                    'date': date(2013, 12, 4),
                    'amount': Decimal('7.12'),
                    'state': 'edit',
                    'bookingtype': 'mvin',
                    'booktransf': books[2].id,
                    'description': 'Opening Balance',
                }, {
                    'date': date(2013, 12, 5),
                    'amount': Decimal('29.00'),
                    'description': '05.12/06.42UHR TT TELTOW',
                    'state': 'edit',
                    'bookingtype': 'mvout',
                    'booktransf': books[1].id,
                    'description': 'GA NR00002168 BLZ10000000 0; 05.12/06.42UHR TT TELTOW',
                }, {
                    'date': date(2013, 12, 5),
                    'amount': Decimal('56.37'),
                    'description': 'some food',
                    'state': 'check',
                    'bookingtype': 'out',
                    'party': parties[2].id,
                    'category': categories[0].id,
                }, {
                    'date': date(2020, 10, 22),
                    'amount': Decimal('55.84'),
                    'description': 'Lebensmittel',
                    'state': 'edit',
                    'bookingtype': 'spout',
                    'category': categories[0].id,
                    'party': parties[3].id,
                    'splitlines': [
                        ('create', [{
                                'splittype': 'cat',
                                'amount': Decimal('49.36'),
                                'description': 'Lebensmittel',
                                'category': categories[0].id,
                            }, {
                                'splittype': 'cat',
                                'amount': Decimal('2.99'),
                                'description': 'Klopapier',
                                'category': categories[2].id,
                            }, {
                                'splittype': 'cat',
                                'amount': Decimal('3.49'),
                                'description': 'Sagrotan',
                                'category': categories[1].id,
                            }, {
                                'splittype': 'tr',
                                'amount': Decimal('3.49'),
                                'description': 'transfer out',
                                'booktransf': books[1].id,
                            }],
                        )],
                }])
        Book.write(*[
            [books[0]],
            {
                'lines': [('create', to_create)],
            }])
        self.assertEqual(len(books[0].lines), 4)
        self.assertEqual(books[0].balance, Decimal('-137.58'))

    @with_transaction()
    def test_qiftool_read_transactions(self):
        """ read transaction data from text
        """
        QifTool = Pool().get('cashbook_dataexchange.qiftool')

        result = QifTool.qif_read_transactions('D04.12.2013\nT7,12\nCX\n'+
            'POpening Balance\nL[Bargeld]\n^\nD05.12.2013\nCX\n'+
            'M05.12/06.42UHR TT TELTOW\nT290,00\nPGA NR00002168 BLZ10000000 0\n'+
            'L[S-Giro]\n^\nD05.12.2013\nCX\nMsome food\nT-56,37\n'+
            'PFoodshop Zehlendorf\nLLebensmittel\n^\nD22.10.2020\n'+
            'CX\nMLebensmittel\nT-55,84\nPreal,- Teltow\nLLebensmittel\n'+
            'SLebensmittel\nELebensmittel\n$-49,36\nSKosmetik\nEKlopapier\n'+
            '$-2,99\nSHaushaltschemie\nESagrotan\n$-3,49\n^\n')
        self.assertEqual(result, [{
                'split': [],
                'date': date(2013, 12, 4),
                'amount': Decimal('7.12'),
                'state': 'check',
                'party': 'Opening Balance',
                'account': 'Bargeld',
            }, {
                'split': [],
                'date': date(2013, 12, 5),
                'state': 'check',
                'description': '05.12/06.42UHR TT TELTOW',
                'amount': Decimal('290.00'),
                'party': 'GA NR00002168 BLZ10000000 0',
                'account': 'S-Giro',
            }, {
                'split': [],
                'date': date(2013, 12, 5),
                'state': 'check',
                'description': 'some food',
                'amount': Decimal('-56.37'),
                'party': 'Foodshop Zehlendorf',
                'category': 'Lebensmittel',
            }, {
                'split': [{
                        'category': 'Lebensmittel',
                        'description': 'Lebensmittel',
                        'amount': Decimal('-49.36'),
                    }, {
                        'category': 'Kosmetik',
                        'description': 'Klopapier',
                        'amount': Decimal('-2.99'),
                    }, {
                        'category': 'Haushaltschemie',
                        'description': 'Sagrotan',
                        'amount': Decimal('-3.49'),
                    }],
                'date': date(2020, 10, 22),
                'state': 'check',
                'description': 'Lebensmittel',
                'amount': Decimal('-55.84'),
                'party': 'real,- Teltow',
                'category': 'Lebensmittel',
            }])

    @with_transaction()
    def test_qiftool_read_categories(self):
        """ read category-data from text
        """
        QifTool = Pool().get('cashbook_dataexchange.qiftool')

        result = QifTool.qif_read_categories('NGehalt\nI\n^\nNGehalt:Zulagen\nI\n^'+
            'NTelekommunikation\nE\n^\nNTelekommunikation:Online-Dienste\nE\n^')
        self.assertEqual(result, {
            'in': {
                'Gehalt': {
                    'type': 'in',
                    'childs': {
                        'Zulagen': {
                            'type': 'in',
                            'childs': {},
                            },
                        },
                    },
                },
            'out': {
                'Telekommunikation': {
                    'type': 'out',
                    'childs': {
                        'Online-Dienste': {
                            'type': 'out',
                            'childs': {},
                            },
                        },
                    },
                },
            })

# end CategoryTestCase

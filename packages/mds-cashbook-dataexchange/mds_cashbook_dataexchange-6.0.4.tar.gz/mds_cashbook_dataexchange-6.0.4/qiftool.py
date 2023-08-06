# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import Pool
from trytond.model import Model
from trytond.i18n import gettext
from trytond.report import Report
from decimal import Decimal
from datetime import datetime


class QifTool(Model):
    'QIF Tool'
    __name__ = 'cashbook_dataexchange.qiftool'

    @classmethod
    def split_by_type(cls, qifdata):
        """ split file-content by type
        """
        lines = qifdata.split('\n')

        blocks = {}
        current_type = None
        for line in lines:
            if line.startswith('!Type:'):
                current_type = line[len('!Type:'):].strip()
            else :
                if current_type is None:
                    continue

                if not current_type in blocks.keys():
                    blocks[current_type] = []
                blocks[current_type].append(line.strip())

        for block in blocks.keys():
            blocks[block] = '\n'.join(blocks[block])
        return blocks

    @classmethod
    def get_amount_from_txt(cls, amount_txt):
        """ convert text to Decimal
        """
        if (',' in amount_txt) and (amount_txt[-3] == '.'):
            # '.' = decimal, ',' = tousand
            amount_txt = amount_txt.replace(',', '.')
        elif ('.' in amount_txt) and (amount_txt[-3] == ','):
            # ',' = decimal, '.' = tousand
            amount_txt = amount_txt.replace('.', '')
            amount_txt = amount_txt.replace(',', '.')
        elif ',' in amount_txt:
            amount_txt = amount_txt.replace(',', '.')
        return Decimal(amount_txt)

    @classmethod
    def qif_read_transactions(cls, transactiondata):
        """ read transactions from text
            result: [{
                'split': [{
                    'amount': <Decimal>,
                    'description': 'purpose',
                    'category': 'name of categroy',
                    },...],
                'date': <date of transaction>,
                'amount': <Decimal>,
                'party': 'name of party',
                'address': 'address of party',
                'checknumber': 'number',
                'description': 'purpose',
                'state': 'check|edit',
                'account': 'name of cashbook',
                'category': 'name of category',
                }, ...]
        """
        result = []
        for booktxt in transactiondata.split('^'):
            if len(booktxt.strip()) == 0:
                continue

            booking = {'split': []}
            for line in booktxt.strip().split('\n'):
                line_txt = line[1:].strip()
                if line.startswith('D'):        # date
                    booking['date'] = datetime.strptime(line_txt, '%d.%m.%Y').date()
                elif line.startswith('T'):      # total
                    booking['amount'] = cls.get_amount_from_txt(line_txt)
                elif line.startswith('U'):      # total
                    booking['amount'] = cls.get_amount_from_txt(line_txt)
                elif line.startswith('P'):      # party
                    booking['party'] = line_txt
                elif line.startswith('A'):      # address
                    booking['address'] = line_txt
                elif line.startswith('N'):      # address
                    booking['checknumber'] = line_txt
                elif line.startswith('M'):      # memo
                    booking['description'] = line_txt
                elif line.startswith('C'):      # state
                    booking['state'] = {
                            'X': 'check',
                            '*': 'edit',
                        }.get(line_txt, 'edit')
                elif line.startswith('L'):      # category, account
                    if line_txt.startswith('[') and line_txt.endswith(']'):
                        booking['account'] = line_txt[1:-1]
                    else :
                        booking['category'] = line_txt
                elif line.startswith('S'):      # split: category, account
                    if line_txt.startswith('[') and line_txt.endswith(']'):
                        booking['split'].append({
                            'account': line_txt[1:-1],
                            })
                    else :
                        booking['split'].append({
                            'category': line_txt,
                            })
                elif line.startswith('E'):      # split: memo
                    booking['split'][-1]['description'] = line_txt
                elif line.startswith('$'):      # split: amount
                    booking['split'][-1]['amount'] = cls.get_amount_from_txt(line_txt)
                elif line.startswith('£'):      # split: amount
                    booking['split'][-1]['amount'] = cls.get_amount_from_txt(line_txt)
                else :
                    raise ValueError('unknown line-code: %s' % (line))
            result.append(booking)
        return result

    @classmethod
    def qif_export_book(cls, book):
        """ export book
        """
        result = ['!Type:Bank']

        def get_amount_by_bookingstate(amount, line):
            """ get amount with sign
            """
            if line.bookingtype in ['in', 'spin', 'mvin']:
                return amount
            elif line.bookingtype in ['out', 'spout', 'mvout']:
                return amount * Decimal('-1.0')
            else :
                raise ValueError('invalid bookingtype: %s' % line.bookingtype)

        for line in book.lines:
            # date
            result.append('D%(date)s' % {
                'date': Report.format_date(line.date, None),
                })
            # total
            result.append('T%(total)s' % {
                'total': Report.format_number(get_amount_by_bookingstate(line.amount, line), None),
                })
            # state
            result.append('C%(state)s' % {
                'state': 'X' if line.state in ['check', 'done'] else '*',
                })
            # party
            if line.party:
                result.append('P%(party)s' % {
                    'party': line.party.rec_name,
                    })
                # address
                p_address = line.party.address_get()
                if p_address:
                    if len(p_address.full_address.strip()) > 0:
                        result.append('A%(address)s' % {
                            'address': p_address.full_address.replace('\n', ', ').strip(),
                            })
            # category
            if line.category:
                result.append('L%(category)s' % {
                    'category': line.category.rec_name.replace('/', ':'),
                    })
            # account
            if line.booktransf:
                result.append('L[%(account)s]' % {
                    'account': line.booktransf.name,
                    })
            # description
            if line.description:
                result.append('M%(memo)s' % {
                    'memo': line.description.replace('\n', '; ')
                    })

            # split-booking
            for splitline in line.splitlines:
                result.append('S%(category)s' % {
                    'category': splitline.category.rec_name.replace('/', ':'),
                    })
                if splitline.description:
                    result.append('E%(memo)s' % {
                        'memo': splitline.description.replace('\n', '; ')
                        })
                result.append('$%(total)s' % {
                    'total': Report.format_number(get_amount_by_bookingstate(splitline.amount, line), None),
                    })
            result.append('^')
        return '\n'.join(result)

    @classmethod
    def get_party_by_name(cls, partyname):
        """ find party
        """
        Party = Pool().get('party.party')

        party_id = None
        msg_txt = None

        parties = Party.search([('rec_name', 'ilike', '%%%s%%' % partyname)])
        if len(parties) == 0:
            msg_txt = gettext(
                'cashbook_dataexchange.mds_import_party_notfound',
                pname = partyname,
                )
        elif len(parties) == 1:
            party_id = parties[0].id
        else :
            party_id = parties[0].id
            msg_txt = gettext(
                'cashbook_dataexchange.mds_import_many_parties_found',
                pname = partyname,
                pname2 = parties[0].rec_name,
                )
        return (party_id, msg_txt)

    @classmethod
    def get_account_by_name(cls, book, account_name):
        """ find cashbook
        """
        Book = Pool().get('cashbook.book')

        book_obj = None
        msg_txt = None
        books = Book.search([
                ('name', '=', account_name),
                ('owner.id', '=', book.owner.id),
                ('id', '!=', book.id),
            ])
        if len(books) == 1:
            book_obj = books[0]
        elif len(books) == 0:
            msg_txt = gettext(
                'cashbook_dataexchange.mds_import_book_notfound',
                bookname = account_name,
                )
        else :
            msg_txt = gettext(
                'cashbook_dataexchange.mds_import_many_books_found',
                bookname1 = account_name,
                bookname2 = books[0].rec_name,
                )
            book_obj = books[0]
        return (book_obj, msg_txt)

    @classmethod
    def get_category_by_name(cls, company, catname):
        """ find category
        """
        Category = Pool().get('cashbook.category')

        cat_obj = None
        msg_txt = None
        categories = Category.search([
                ('rec_name', '=', catname.replace(':', '/')),
                ('company.id', '=', company.id),
            ])
        if len(categories) == 1:
            cat_obj = categories[0]
        elif len(categories) == 0:
            msg_txt = gettext(
                'cashbook_dataexchange.mds_import_category_notfound',
                catname = catname,
                )
        else :
            msg_txt = gettext(
                'cashbook_dataexchange.mds_import_many_categories_found',
                catname1 = catname,
                catname2 = '%(name)s [%(type)s]' % {
                    'name': categories[0].rec_name,
                    'type': categories[0].cattype,
                    },
                )
            cat_obj = categories[0]
        return (cat_obj, msg_txt)

    @classmethod
    def convert_categories_to_create(cls, cat_tree):
        """ cat_tree: result from cls.qif_read_categories()
        """
        Category = Pool().get('cashbook.category')

        def get_create(ctype, catdict, parent, do_search):
            """ check if category exists, generate create-data
            """
            result = []
            for catname in catdict.keys():
                if do_search == True:
                    c_lst = Category.search([
                            ('cattype', '=', ctype),
                            ('name', '=', catname),
                            ('parent', '=', None) if parent is None else ('parent.id', '=', parent.id),
                        ])
                else :
                    c_lst = []

                if len(c_lst) == 0:
                    cat1 = {
                        'cattype': ctype,
                        'name': catname,
                        }
                    if parent is not None:
                        cat1['parent'] = parent.id

                    if len(catdict[catname]['childs']) > 0:
                        childs = get_create(ctype, catdict[catname]['childs'], None, False)
                        if len(childs) > 0:
                            cat1['childs'] = [('create', childs)]
                    result.append(cat1)
                else :
                    if len(catdict[catname]['childs']) > 0:
                        result.extend(get_create(ctype, catdict[catname]['childs'], c_lst[0], True))
            return result
        to_create = []
        for typ1 in ['in', 'out']:
            to_create.extend(get_create(typ1, cat_tree[typ1], None, True))
        return to_create

    @classmethod
    def convert_parties_to_create(cls, transactions):
        """ extract party from transaction, check if exist,
            create 'to_create'
        """
        Party = Pool().get('party.party')

        to_create = []
        party_cache = []
        for transaction in transactions:
            if 'party' in transaction.keys():
                if transaction['party'] in party_cache:
                    continue

                party_cache.append(transaction['party'])
                if Party.search_count([
                        ('rec_name', 'ilike', '%%%(pname)s%%' % {
                            'pname': transaction['party'],
                            })
                    ]) == 0:
                    to_create.append({
                        'name': transaction['party'],
                        'addresses': [('create', [{
                            'street': transaction.get('address', None),
                            }])],
                        })
        return to_create

    @classmethod
    def check_counter_transaction(cls, book, line):
        """ check if planned transaction was already inserted by
            import to target-cashbook
        """
        Line = Pool().get('cashbook.line')

        if Line.search_count([
            ('cashbook.id', '=', book.id),
            ('booktransf.id', '=', line['booktransf']),
            ('date', '=', line['date']),
            #('description', '=', line['description']),
            ('amount', '=', line['amount']),
            ('bookingtype', '=', line['bookingtype']),
            ]) > 0:
            return True
        else :
            return False

    @classmethod
    def get_category_account(cls, book, transaction):
        """ get category or account
        """
        cat_name = transaction.get('category', None)
        account_name = transaction.get('account', None)
        msg_list = []
        fail_cnt = 0
        category = account = None
        if cat_name is not None:
            (category, msg_txt) = cls.get_category_by_name(book.company, cat_name)
            if category is None:
                msg_list.append(msg_txt)
                fail_cnt += 1
        elif account_name is not None:
            (account, msg_txt) = cls.get_account_by_name(book, account_name)
            if account is None:
                msg_list.append(msg_txt)
                fail_cnt += 1
        return (category, account, msg_list, fail_cnt)

    @classmethod
    def convert_transactions_to_create(cls, book, transactions, split2edit=True):
        """ convert read transactions to create-command
            split2edit: True = split-bookings are 'edit', False = dont change
        """
        def updt_description(descr_txt):
            """ repair line breaks
            """
            if descr_txt is None:
                return None
            return descr_txt.replace('\\n', '\n')

        to_create = []
        msg_list = []
        fail_cnt = 0
        for transaction in transactions:
            line = {x:transaction[x] for x in [
                    'date', 'amount', 'description', 'state',
                ] if x in transaction.keys()}

            if 'description' in line.keys():
                line['description'] = updt_description(line['description'])

            (category, account, msg_lst2, fail_cnt2) = cls.get_category_account(book, transaction)
            msg_list.extend(msg_lst2)
            if fail_cnt2 > 0:
                fail_cnt += fail_cnt2
                continue

            if category:
                cat_type = category.cattype
                line['category'] = category.id

                if cat_type == 'out':
                    # amount of usually out-transaction are negative in QIF,
                    # if its a return-transaction it should be positive
                    line['amount'] = line['amount'].copy_negate()

                line['bookingtype'] = cat_type
                if len(transaction['split']) > 0:
                    line['bookingtype'] = {
                            'in': 'spin',
                            'out': 'spout',
                        }[cat_type]
            elif account:
                if line['amount'] < Decimal('0.0'):
                    line['bookingtype'] = 'mvout'
                    line['amount'] = line['amount'].copy_negate()
                else :
                    line['bookingtype'] = 'mvin'

                line['booktransf'] = account.id
                descr_lst = [transaction.get('party', '-')]
                if 'description' in line.keys():
                    descr_lst.append(line['description'])
                if 'party' in transaction.keys():
                    del transaction['party']
                line['description'] = '; '.join(descr_lst)
                line['state'] = 'edit'
                if cls.check_counter_transaction(book, line) == True:
                    # counter-transaction already exists
                    continue
            else :
                # transaction: no category, no account - ignore?
                if line.get('amount', Decimal('0.0')) == Decimal('0.0'):
                    # no amount --> ignore!
                    tr_info = {'trdate': '-', 'amount':'-'}
                    if 'date' in transaction.keys():
                        tr_info['trdate']  = Report.format_date(transaction['date'], None)
                    if 'amount' in transaction.keys():
                        tr_info['amount']  = Report.format_currency(
                            transaction['amount'],
                            None,
                            book.currency)
                    tr_info['descr'] = transaction.get('description', '-')
                    msg_list.append(gettext(
                        'cashbook_dataexchange.msg_ignore_null_booking',
                        trinfo = '%(trdate)s, %(amount)s, %(descr)s' % tr_info,
                        ))
                    continue

            # party
            if 'party' in transaction.keys():
                (party_id, msg_txt) = cls.get_party_by_name(transaction['party'])
                if party_id is not None:
                    line['party'] = party_id
                else :
                    fail_cnt += 1
                if msg_txt is not None:
                    msg_list.append(msg_txt)

            for x in ['address', 'checknumber']:
                if x in transaction.keys():
                    line['description'] = ', '.join([
                        line.get('description', ''),
                        '%s %s' % (
                            gettext('cashbook_dataexchange.mds_import_%s' % x),
                            transaction[x]
                            ),
                        ])

            split_lines = []
            for sp_line in transaction['split']:
                (category, account, msg_lst2, fail_cnt2) = cls.get_category_account(book, sp_line)
                msg_list.extend(msg_lst2)
                if fail_cnt2 > 0:
                    fail_cnt += fail_cnt2
                    continue

                split_line = {
                    'amount': sp_line['amount'] \
                        if line['bookingtype'].endswith('in') else sp_line['amount'].copy_negate(),
                    'description': updt_description(sp_line.get('description', None)),
                    }

                if category:
                    # category match to bookingtype?
                    if ((category.cattype == 'in') and line['bookingtype'].endswith('out')) or\
                        ((category.cattype == 'out') and line['bookingtype'].endswith('in')):
                        msg_list.append(gettext(
                            'cashbook_dataexchange.mds_import_category_not_match',
                            catname = '%s [%s]' % (category.rec_name, category.cattype),
                            bktype = line['bookingtype'],
                            data = str(transaction),
                            ))
                        fail_cnt += 1
                        continue
                    split_line['splittype'] = 'cat'
                    split_line['category'] = category.id
                elif account:
                    split_line['splittype'] = 'tr'
                    split_line['booktransf'] = account.id
                else :
                    continue

                split_lines.append(split_line)

            if len(split_lines) > 0:
                line['splitlines'] = [('create', split_lines)]

            if split2edit == True:
                if 'splitlines' in line.keys():
                    line['state'] = 'edit'

            # check data
            if line['bookingtype'] in ['in', 'out']:
                if line.get('category', None) is None:
                    msg_list.append(gettext(
                        'cashbook_dataexchange.mds_import_no_category',
                        trdata = str(transaction)))
                    fail_cnt += 1
            elif line['bookingtype'] in ['mvin', 'mvout']:
                if line.get('booktransf', None) is None:
                    msg_list.append(gettext(
                        'cashbook_dataexchange.mds_import_no_account',
                        trdata = str(transaction)))
                    fail_cnt += 1

            to_create.append(line)
        return (to_create, msg_list, fail_cnt)

    @classmethod
    def qif_read_categories(cls, catdata):
        """ read categories from text
            result: {
                'in': [{
                    '<Category-Name>': {
                        'type': 'in|out',
                        'childs': [...],
                        },
                    },...],
                'out': [{},...],
                }
        """
        def add_category(catdict, namelst, ctype):
            """ add category to dict
            """
            if not namelst[0] in catdict.keys():
                catdict[namelst[0]] = {'type': ctype, 'childs': {}}

            if len(namelst) > 1:
                catdict[namelst[0]]['childs'] = add_category(
                    catdict[namelst[0]]['childs'],
                    namelst[1:],
                    ctype)
            return catdict

        categories = {'in': {}, 'out': {}}
        for cattxt in catdata.split('^'):
            if len(cattxt.strip()) == 0:
                continue
            catname = None
            cattype = None
            for line in cattxt.strip().split('\n'):
                if line.startswith('N'):
                    catname = line[1:].strip().split(':')
                elif line.startswith('E'):
                    cattype = 'out'
                elif line.startswith('I'):
                    cattype = 'in'
                else :
                    raise ValueError('invalid line: %s (%s)' % (line, cattxt))
            categories[cattype] = add_category(categories[cattype], catname, cattype)
        return categories

    @classmethod
    def qif_export_category(cls, record):
        """ export single category as qif
        """
        return '\n'.join([
            'N%(cname)s' % {
                'cname': record.rec_name.replace('/', ':'),
                },
            'E' if record.cattype == 'out' else 'I',
            '^',
            ])

# end QifTool

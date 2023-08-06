# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.transaction import Transaction
from trytond.i18n import gettext
from trytond.pyson import Eval, Bool
from trytond.report import Report
from decimal import Decimal


class ImportQifWizardStart(ModelView):
    'Import QIF-File'
    __name__ = 'cashbook_dataexchange.qif_imp_wiz.start'

    company = fields.Many2One(model_name='company.company',
        string="Company", required=True,
        states={'invisible': True})
    book = fields.Many2One(string='Cashbook', readonly=True,
        model_name='cashbook.book',
        states={
            'invisible': ~Bool(Eval('book')),
        })
    file_ = fields.Binary(string="QIF-File", required=True,
        help='Quicken Interchange Format')

    @classmethod
    def default_company(cls):
        return Transaction().context.get('company')

# end ImportQifWizardStart


class ImportQifWizardInfo(ModelView):
    'Import QIF-File'
    __name__ = 'cashbook_dataexchange.qif_imp_wiz.info'

    company = fields.Many2One(model_name='company.company',
        string="Company", required=True,
        states={'invisible': True})
    book = fields.Many2One(string='Cash Book', readonly=True,
        model_name='cashbook.book',
        states={
            'invisible': ~Bool(Eval('book')),
        })
    allowimport = fields.Boolean(string='Import Enabled',
        states={'invisible': True})
    info = fields.Text(string='Information', readonly=True)

# end ImportQifWizardInfo


class ImportQifWizard(Wizard):
    'Import QIF-File'
    __name__ = 'cashbook_dataexchange.qif_imp_wiz'

    start_state = 'start'
    start = StateView(model_name='cashbook_dataexchange.qif_imp_wiz.start', \
        view='cashbook_dataexchange.qif_imp_wiz_start_form', \
        buttons=[
            Button(string='Cancel', state='end', icon='tryton-cancel'),
            Button(string='Read File', state='readf', icon='tryton-forward', default=True),
            ])
    showinfo = StateView(model_name='cashbook_dataexchange.qif_imp_wiz.info', \
        view='cashbook_dataexchange.qif_imp_wiz_info_form', \
        buttons=[
            Button(string='Cancel', state='end', icon='tryton-cancel'),
            Button(string='Import Data', state='importf', icon='tryton-import', default=True,
                states={
                    'readonly': Eval('allowimport', False) == False,
                }),
            ])

    readf = StateTransition()
    importf = StateTransition()

    def default_start(self, fields):
        """ show book, company
        """
        context = Transaction().context

        values = {
            'company': Transaction().context.get('company'),
            'book': None,
            }

        model = context.get('active_model', '')
        if model == 'cashbook.book':
            values['book'] = context.get('active_id', None)
        return values

    def default_showinfo(self, fields):
        """ show import-info
        """
        values = {
            'company': self.start.company.id,
            'info': getattr(self.showinfo, 'info', None),
            'book': getattr(getattr(self.start, 'book', None), 'id', None),
            'allowimport': getattr(self.showinfo, 'allowimport', False),
            }
        return values

    def transition_readf(self):
        """ read file, show number of objects
        """
        pool = Pool()
        QifTool = pool.get('cashbook_dataexchange.qiftool')
        Category = pool.get('cashbook.category')

        model = Transaction().context.get('active_model', '')
        file_content = None
        if isinstance(self.start.file_, bytes):
            file_content = self.start.file_.decode('utf8')

        self.showinfo.allowimport = False
        if model == 'cashbook.category':
            def get_catlist(record, cattype, parent_name=None):
                """ generate list of categories
                """
                names = []

                if record['cattype'] != cattype:
                    return []

                if 'parent' in record.keys():
                    parent_name = Category(record['parent']).rec_name

                name_lst = []
                if parent_name:
                    name_lst.append(parent_name)
                name_lst.append(record['name'])
                current_name = '/'.join(name_lst)
                names.append(current_name)

                if 'childs' in record.keys():
                    # record['childs']: [('create', [{}, ...]))]
                    for x in record['childs'][0][1]:
                        names.extend(get_catlist(x, cattype, current_name))
                return names

            # read file content, extract categories
            qif_content = QifTool.split_by_type(file_content)
            if 'Cat' in qif_content.keys():
                to_create = QifTool.convert_categories_to_create(QifTool.qif_read_categories(qif_content['Cat']))

                in_categories = []
                out_categories = []
                for x in to_create:
                    in_categories.extend(get_catlist(x, 'in'))
                    out_categories.extend(get_catlist(x, 'out'))

                self.showinfo.info = gettext(
                    'cashbook_dataexchange.msg_wiz_categories_found',
                    categories = '\n'.join(
                        [''] +
                        ['%s (in)' % x for x in in_categories]+
                        [''] +
                        ['%s (out)' % x for x in out_categories]
                        )
                    )
                if len(to_create) > 0:
                    self.showinfo.allowimport = True
            else :
                self.showinfo.info = gettext('cashbook_dataexchange.msg_wiz_no_categories')
        elif model == 'party.party':
            # read file content, extract parties
            qif_content = QifTool.split_by_type(file_content)
            if 'Bank' in qif_content.keys():
                to_create = QifTool.convert_parties_to_create(
                        QifTool.qif_read_transactions(qif_content['Bank'])
                    )
                self.showinfo.info = gettext(
                    'cashbook_dataexchange.msg_wiz_parties_found',
                    numparties = len(to_create),
                    ) + '\n\n' + '\n'.join([x['name'] for x in to_create])
                if len(to_create) > 0:
                    self.showinfo.allowimport = True
            else :
                self.showinfo.info = gettext('cashbook_dataexchange.msg_wiz_no_bank')
        elif model == 'cashbook.book':
            info_lst = []
            # read file content, extract categories
            qif_content = QifTool.split_by_type(file_content)
            if 'Bank' in qif_content.keys():
                (to_create, msg_list, fail_cnt) = QifTool.convert_transactions_to_create(
                        self.start.book,
                        QifTool.qif_read_transactions(qif_content['Bank'])
                    )
                if len(msg_list) > 0:
                    info_lst.append(gettext('cashbook_dataexchange.msg_wiz_transactions_error'))
                    info_lst.append('')

                    short_lst = []
                    for x in msg_list:
                        if x not in short_lst:
                            short_lst.append(x)
                    info_lst.extend(short_lst)
                    info_lst.append('')

                # count
                if fail_cnt == 0:
                    debit = sum([x['amount'] for x in to_create if x['bookingtype'] in ['out', 'mvout', 'spout']])
                    credit = sum([x['amount'] for x in to_create if x['bookingtype'] in ['in', 'mvin', 'spin']])
                    balance = credit - debit

                    if len(msg_list) > 0:
                        msg_list.append('')
                    info_lst.append(gettext(
                        'cashbook_dataexchange.msg_wiz_transactions_found',
                        quantity = len(to_create),
                        balance = Report.format_currency(balance, None, self.start.book.currency),
                        credit = Report.format_currency(credit, None, self.start.book.currency),
                        debit = Report.format_currency(debit, None, self.start.book.currency),
                        ))
                    self.showinfo.allowimport = True
            else :
                info_lst.append(gettext('cashbook_dataexchange.msg_wiz_no_bank'))
            self.showinfo.info = '\n'.join(info_lst)

        return 'showinfo'

    def transition_importf(self):
        """ read file, show number of objects
        """
        pool = Pool()
        Category = pool.get('cashbook.category')
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Party = pool.get('party.party')
        QifTool = pool.get('cashbook_dataexchange.qiftool')

        model = Transaction().context.get('active_model', '')
        file_content = None
        if isinstance(self.start.file_, bytes):
            file_content = self.start.file_.decode('utf8')

        if model == 'cashbook.category':
            if file_content:
                records = Category.create_from_qif(file_content)
        elif model == 'cashbook.book':
            if file_content:
                Book.create_from_qif(self.showinfo.book, file_content)
                lines = Line.search([
                        ('cashbook.id', '=', self.showinfo.book.id),
                        ('state', '=', 'edit'),
                    ])
                if len(lines) > 0:
                    Line.wfcheck(lines)
        elif model == 'party.party':
            qif_content = QifTool.split_by_type(file_content)
            if 'Bank' in qif_content.keys():
                to_create = QifTool.convert_parties_to_create(
                        QifTool.qif_read_transactions(qif_content['Bank'])
                    )
                Party.create(to_create)
        return 'end'

# end ImportQifWizard


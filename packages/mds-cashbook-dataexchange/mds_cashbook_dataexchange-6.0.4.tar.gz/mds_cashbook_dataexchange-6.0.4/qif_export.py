# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.report import Report
from trytond.pool import Pool
from slugify import slugify



class QifCategoryExport(Report):
    __name__ = 'cashbook_dataexchange.rep_category'

    @classmethod
    def execute(cls, ids, data):
        """ filename for export
        """
        pool = Pool()
        IrDate = pool.get('ir.date')
        Category = pool.get('cashbook.category')

        return (
            'qif',
            Category.export_as_qif(),
            False,
            '%s-categories' % IrDate.today().isoformat().replace('-', ''))

# end QifCategoryExport


class QifBookExport(Report):
    __name__ = 'cashbook_dataexchange.rep_book'

    @classmethod
    def execute(cls, ids, data):
        """ filename for export
        """
        pool = Pool()
        IrDate = pool.get('ir.date')
        Book = pool.get('cashbook.book')

        books =  Book.search([('id', '=', data.get('id', -1))])
        if len(books) == 1:
            return (
                'qif',
                Book.export_as_qif(books[0]),
                False,
                slugify('%(date)s-transactions-%(book)s' % {
                    'date': IrDate.today().isoformat().replace('-', ''),
                    'book': books[0].name,
                    }, max_length=100, word_boundary=True, save_order=True),
                )
        else :
            return (
                'txt',
                'not cashbook found',
                False,
                '%(date)s-transactions-%(book)s' % {
                    'date': IrDate.today().isoformat().replace('-', ''),
                    'book': 'not-found',
                    })

# end QifBookExport

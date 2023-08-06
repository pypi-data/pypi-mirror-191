# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta


class Book(metaclass=PoolMeta):
    __name__ = 'cashbook.book'

    @classmethod
    def export_as_qif(cls, book):
        """ export all transactions as QIF
        """
        pool = Pool()
        QifTool = pool.get('cashbook_dataexchange.qiftool')

        return QifTool.qif_export_book(book)

    @classmethod
    def create_from_qif(cls, book, qifdata):
        """ add transactions from QIF-File-content
        """
        pool = Pool()
        QifTool = pool.get('cashbook_dataexchange.qiftool')
        Book2 = pool.get('cashbook.book')

        qif_content = QifTool.split_by_type(qifdata)
        if not 'Bank' in qif_content.keys():
            return None

        (to_create, msg_list, fail_cnt) = QifTool.convert_transactions_to_create(
                book,
                QifTool.qif_read_transactions(qif_content['Bank'])
            )
        if fail_cnt == 0:
            Book2.write(*[
                [book],
                {
                    'lines': [('create', to_create)],
                }])
            return [book]
        return None

# end Category

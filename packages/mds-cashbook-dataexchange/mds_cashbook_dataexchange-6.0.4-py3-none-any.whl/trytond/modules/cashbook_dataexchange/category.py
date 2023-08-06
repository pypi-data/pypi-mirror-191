# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta


class Category(metaclass=PoolMeta):
    __name__ = 'cashbook.category'

    @classmethod
    def export_as_qif(cls):
        """ export all accessible categories as QIF
        """
        pool = Pool()
        Category2 = pool.get('cashbook.category')
        QifTool = pool.get('cashbook_dataexchange.qiftool')

        categories = Category2.search([],
            order=[('cattype', 'ASC'), ('rec_name', 'ASC')])

        export = ['!Type:Cat']
        export.extend([QifTool.qif_export_category(x) for x in categories])
        return '\n'.join(export)

    @classmethod
    def create_from_qif(cls, qifdata):
        """ add categories from QIF-File-content
        """
        pool = Pool()
        QifTool = pool.get('cashbook_dataexchange.qiftool')
        Category2 = pool.get('cashbook.category')

        type_data = QifTool.split_by_type(qifdata)
        if not 'Cat' in type_data.keys():
            return None

        to_create = QifTool.convert_categories_to_create(
            QifTool.qif_read_categories(type_data['Cat']))
        return Category2.create(to_create)

# end Category

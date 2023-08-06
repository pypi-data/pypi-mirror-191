# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import Pool
from .category import Category
from .book import Book
from .qiftool import QifTool
from .qif_import_wiz import ImportQifWizard, ImportQifWizardStart, ImportQifWizardInfo
from .qif_export import QifCategoryExport, QifBookExport

def register():
    Pool.register(
        QifTool,
        Category,
        Book,
        ImportQifWizardStart,
        ImportQifWizardInfo,
        module='cashbook_dataexchange', type_='model')
    Pool.register(
        QifCategoryExport,
        QifBookExport,
        module='cashbook_dataexchange', type_='report')
    Pool.register(
        ImportQifWizard,
        module='cashbook_dataexchange', type_='wizard')

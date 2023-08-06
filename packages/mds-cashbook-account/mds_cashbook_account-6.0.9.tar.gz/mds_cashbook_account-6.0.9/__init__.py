# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import Pool
from .category import Category
from .book import Book
from .configuration import Configuration, UserConfiguration
from .line import Line
from .tax import TaxLine
from .move import Move, MoveLine
from .splitline import SplitLine

def register():
    Pool.register(
        Configuration,
        UserConfiguration,
        Category,
        Book,
        Line,
        TaxLine,
        SplitLine,
        Move,
        MoveLine,
        module='cashbook_account', type_='model')

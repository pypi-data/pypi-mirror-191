# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import Pool
from .book import Book
from .line import Line

def register():
    Pool.register(
        Book,
        Line,
        module='cashbook_analytic', type_='model')

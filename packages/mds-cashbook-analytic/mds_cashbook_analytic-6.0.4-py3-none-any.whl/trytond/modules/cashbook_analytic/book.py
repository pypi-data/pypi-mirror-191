# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval


class Book(metaclass=PoolMeta):
    __name__ = 'cashbook.book'

    analytic = fields.Many2One(string='Analytic Account', ondelete='RESTRICT',
        model_name='analytic_account.account', select=True,
        domain=[
            ('company.id', '=', Eval('company', -1)),
            ('type', 'in', ['normal', 'distribution']),
            ],
        depends=['company'])

# end Book

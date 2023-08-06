# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.modules.cashbook_account.tests import CashbookAccountTestCase
from decimal import Decimal
from datetime import date


class AnalyticTestCase(CashbookAccountTestCase):
    'Test cashbook analytic module'
    module = 'cashbook_analytic'

    def prep_analytic_accounts(self, company1):
        """ create root / 001
        """
        AnalyticAccount = Pool().get('analytic_account.account')

        aa_root, = AnalyticAccount.create([{
            'name': 'ROOT',
            'code': 'm-ds',
            'company': company1.id,
            'type': 'root',
            }])

        an_lst = AnalyticAccount.create([{
            'name': 'Food',
            'code': '001',
            'company': company1.id,
            'type': 'normal',
            'root': aa_root.id,
            'parent': aa_root.id,
            }, {
            'name': 'Drink',
            'code': '002',
            'company': company1.id,
            'type': 'normal',
            'root': aa_root.id,
            'parent': aa_root.id,
            }])

        AnalyticAccount.create([{
            'name': 'Distri',
            'code': '003',
            'company': company1.id,
            'type': 'distribution',
            'root': aa_root.id,
            'parent': aa_root.id,
            'distributions': [('create', [{
                    'account': an_lst[0].id,
                    'ratio': Decimal('0.5'),
                }, {
                    'account': an_lst[1].id,
                    'ratio': Decimal('0.5'),
                }]
                )],
            }])

    @with_transaction()
    def test_analytic_line_check_wf_in_booking_normal(self):
        """ create cashbook + line + analytic-account,
            check booking in-type, company-currency
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Category = pool.get('cashbook.category')
        Account = pool.get('account.account')
        AccountType = pool.get('account.account.type')
        Journal = pool.get('account.journal')
        Move = pool.get('account.move')
        AnalyticAccount = pool.get('analytic_account.account')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        self.prep_analytic_accounts(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])
            analytic_account, = AnalyticAccount.search([('code', '=', '001')])

            accounts = Account.create([{
                'name': 'Account Book',
                'code': '0123',
                'type': acc_type.id,
                }, {
                'name': 'Account Category',
                'code': '2345',
                'type': acc_type.id,
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Account Book')
            self.assertEqual(accounts[0].type.currency.code, 'usd')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'usd')
            self.assertEqual(company.currency.code, 'usd')

            category2, = Category.create([{
                'company': company.id,
                'name': 'In-Category',
                'cattype': 'in',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                'analytic': analytic_account.id,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'sell something',
                        'category': category2.id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.analytic.rec_name, '001 - Food')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 2)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(moves[0].lines[0].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(len(moves[0].lines[0].analytic_lines), 1)
            self.assertEqual(moves[0].lines[0].analytic_lines[0].account.rec_name, '001 - Food')
            self.assertEqual(moves[0].lines[0].analytic_lines[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].lines[0].analytic_lines[0].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].analytic_lines[0].debit, Decimal('0.0'))

            self.assertEqual(moves[0].lines[1].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(len(moves[0].lines[1].analytic_lines), 0)

            # delete move
            Line.wfedit([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 0)

            # create move again
            Line.wfcheck([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'draft')

            # post move
            Line.wfdone([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'posted')

    @with_transaction()
    def test_analytic_line_check_wf_in_booking_distri(self):
        """ create cashbook + line + analytic-account (distribution),
            check booking in-type, company-currency
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Category = pool.get('cashbook.category')
        Account = pool.get('account.account')
        AccountType = pool.get('account.account.type')
        Journal = pool.get('account.journal')
        Move = pool.get('account.move')
        AnalyticAccount = pool.get('analytic_account.account')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        self.prep_analytic_accounts(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])
            analytic_account, = AnalyticAccount.search([('code', '=', '003')])

            accounts = Account.create([{
                'name': 'Account Book',
                'code': '0123',
                'type': acc_type.id,
                }, {
                'name': 'Account Category',
                'code': '2345',
                'type': acc_type.id,
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Account Book')
            self.assertEqual(accounts[0].type.currency.code, 'usd')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'usd')
            self.assertEqual(company.currency.code, 'usd')

            category2, = Category.create([{
                'company': company.id,
                'name': 'In-Category',
                'cattype': 'in',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                'analytic': analytic_account.id,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'sell something',
                        'category': category2.id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.analytic.rec_name, '003 - Distri')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 2)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(moves[0].lines[0].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(len(moves[0].lines[0].analytic_lines), 2)
            self.assertEqual(moves[0].lines[0].analytic_lines[0].account.rec_name, '001 - Food')
            self.assertEqual(moves[0].lines[0].analytic_lines[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].lines[0].analytic_lines[0].credit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[0].analytic_lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].analytic_lines[1].account.rec_name, '002 - Drink')
            self.assertEqual(moves[0].lines[0].analytic_lines[1].date, date(2022, 5, 5))
            self.assertEqual(moves[0].lines[0].analytic_lines[1].credit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[0].analytic_lines[1].debit, Decimal('0.0'))

            self.assertEqual(moves[0].lines[1].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(len(moves[0].lines[1].analytic_lines), 0)

            # delete move
            Line.wfedit([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 0)

            # create move again
            Line.wfcheck([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'draft')

            # post move
            Line.wfdone([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'posted')

# end AnalyticTestCase

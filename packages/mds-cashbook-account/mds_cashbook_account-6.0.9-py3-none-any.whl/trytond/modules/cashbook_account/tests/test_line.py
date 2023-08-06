# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from datetime import date
from decimal import Decimal


class LineTestCase(ModuleTestCase):
    'Test cashbook line module'
    module = 'cashbook_account'

    def prep_line_taxes(self):
        """ prepare taxes
        """
        pool = Pool()
        AccountType = pool.get('account.account.type')
        Account = pool.get('account.account')
        Tax = pool.get('account.tax')

        acc_type, = AccountType.create([{
            'statement': 'balance',
            'name': 'Balance',
            }])
        accounts = Account.create([{
            'name': 'Tax Null',
            'code': '2233',
            'type': acc_type.id,
            }, {
            'name': 'Tax Half',
            'code': '2234',
            'type': acc_type.id,
            }, {
            'name': 'Tax Full',
            'code': '2235',
            'type': acc_type.id,
            }])
        self.assertEqual(accounts[0].rec_name, '2233 - Tax Null')
        self.assertEqual(accounts[1].rec_name, '2234 - Tax Half')
        self.assertEqual(accounts[2].rec_name, '2235 - Tax Full')

        taxes = Tax.create([{
            'name': 'Tax Null',
            'description': 'Tx0',
            'type': 'percentage',
            'rate': Decimal('0.0'),
            'invoice_account': accounts[0].id,
            'credit_note_account': accounts[0].id,
            }, {
            'name': 'Tax Half',
            'description': 'Tx50',
            'type': 'percentage',
            'rate': Decimal('0.1'),
            'invoice_account': accounts[1].id,
            'credit_note_account': accounts[1].id,
            }, {
            'name': 'Tax Full',
            'description': 'Tx100',
            'type': 'percentage',
            'rate': Decimal('0.2'),
            'invoice_account': accounts[2].id,
            'credit_note_account': accounts[2].id,
            }, {
            'name': 'Tax Two',
            'description': 'TxTw',
            'type': 'none',
            'childs': [('create', [{
                'name': 'Part 1',
                'description': 'Part 1 - 8%',
                'type': 'percentage',
                'rate': Decimal('0.08'),
                'invoice_account': accounts[2].id,
                'credit_note_account': accounts[2].id,
                }, {
                'name': 'Part 2',
                'description': 'Part 2 - 10%',
                'type': 'percentage',
                'rate': Decimal('0.1'),
                'invoice_account': accounts[2].id,
                'credit_note_account': accounts[2].id,
                }])],
            }])
        self.assertEqual(len(taxes), 4)
        self.assertEqual(taxes[0].rec_name, 'Tax Null')
        self.assertEqual(taxes[1].rec_name, 'Tax Half')
        self.assertEqual(taxes[2].rec_name, 'Tax Full')
        self.assertEqual(taxes[3].rec_name, 'Tax Two')
        return taxes

    @with_transaction()
    def test_line_check_tax_computation(self):
        """ create line/splitlines, autocreate taxes,
            check amounts in view-fields
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Account = pool.get('account.account')
        Category = pool.get('cashbook.category')
        Configuration = pool.get('cashbook.configuration')
        Journal = pool.get('account.journal')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        with Transaction().set_context({
            'company': company.id,
            }):
            self.prep_accounting(company)
            taxes = self.prep_line_taxes()

            accounts = Account.create([{
                'name': 'Account No 1',
                'code': '0123',
                }, {
                'name': 'Book',
                'code': '4444',
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Account No 1')
            self.assertEqual(accounts[1].rec_name, '4444 - Book')

            self.assertEqual(len(taxes), 4)
            self.assertEqual(taxes[0].rec_name, 'Tax Null')
            self.assertEqual(taxes[1].rec_name, 'Tax Half')
            self.assertEqual(taxes[2].rec_name, 'Tax Full')
            self.assertEqual(taxes[3].rec_name, 'Tax Two')

            categories = Category.create([{
                'company': company.id,
                'name': 'Cat 1',
                'cattype': 'in',
                'account': taxes[1].invoice_account.id,
                'tax0': taxes[3].id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }])
            self.assertEqual(categories[0].rec_name, 'Cat 1 [2234]')

            cfg1 = Configuration()
            cfg1.save()

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[1].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'No Taxes',
                        'category': categories[0].id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }, {
                        'date': date(2022, 5, 2),
                        'description': 'Half Tax',
                        'category': categories[0].id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'ena_tax1': True,
                    }, {
                        'date': date(2022, 5, 3),
                        'description': 'two taxes',
                        'category': categories[0].id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'ena_tax0': True,   # 2x tax
                        'ena_tax1': True,   # 1x tax
                    }, {
                        'date': date(2022, 5, 4),
                        'description': 'Split line - one tax',
                        'category': categories[0].id,
                        'bookingtype': 'spin',
                        'party': party.id,
                        'amount': Decimal('10.0'),
                        'splitlines': [('create', [{
                            'splittype': 'cat',
                            'category': categories[0].id,
                            'amount': Decimal('10.0'),
                            'ena_tax1': True,
                            }])],
                    }, ])],
                }])
            self.assertEqual(book.name, 'Book 1')
            self.assertEqual(book.state, 'open')
            self.assertEqual(len(book.lines), 4)

            self.assertEqual(book.lines[0].rec_name, '05/01/2022|Rev|10.00 usd|No Taxes [Cat 1 [2234]]')
            self.assertEqual(len(book.lines[0].taxes), 0)
            self.assertEqual(book.lines[0].amount_net, None)
            self.assertEqual(book.lines[0].amount_tax0, None)
            self.assertEqual(book.lines[0].amount_tax1, None)
            self.assertEqual(book.lines[0].amount_tax2, None)

            self.assertEqual(book.lines[1].rec_name, '05/02/2022|Rev|10.00 usd|Half Tax [Cat 1 [2234]]')
            self.assertEqual(len(book.lines[1].taxes), 1)
            self.assertEqual(book.lines[1].taxes[0].amount, Decimal('0.91'))
            self.assertEqual(book.lines[1].taxes[0].base, Decimal('9.09'))
            self.assertEqual(book.lines[1].taxes[0].tax.rec_name, 'Tax Half')
            self.assertEqual(book.lines[1].taxes[0].splitline, None)
            self.assertEqual(book.lines[1].amount_net, Decimal('9.09'))
            self.assertEqual(book.lines[1].amount_tax0, None)
            self.assertEqual(book.lines[1].amount_tax1, Decimal('0.91'))
            self.assertEqual(book.lines[1].amount_tax2, None)

            self.assertEqual(book.lines[2].rec_name, '05/03/2022|Rev|10.00 usd|two taxes [Cat 1 [2234]]')
            self.assertEqual(len(book.lines[2].taxes), 3)
            self.assertEqual(book.lines[2].taxes[0].amount, Decimal('0.62'))
            self.assertEqual(book.lines[2].taxes[0].base, Decimal('7.82'))
            self.assertEqual(book.lines[2].taxes[0].tax.rec_name, 'Part 1')
            self.assertEqual(book.lines[2].taxes[0].splitline, None)
            self.assertEqual(book.lines[2].taxes[0].rec_name, 'Part 1 usd0.62 usd7.82')

            self.assertEqual(book.lines[2].taxes[1].amount, Decimal('0.78'))
            self.assertEqual(book.lines[2].taxes[1].base, Decimal('7.82'))
            self.assertEqual(book.lines[2].taxes[1].tax.rec_name, 'Part 2')
            self.assertEqual(book.lines[2].taxes[1].splitline, None)
            self.assertEqual(book.lines[2].taxes[1].rec_name, 'Part 2 usd0.78 usd7.82')

            self.assertEqual(book.lines[2].taxes[2].amount, Decimal('0.78'))
            self.assertEqual(book.lines[2].taxes[2].base, Decimal('7.82'))
            self.assertEqual(book.lines[2].taxes[2].tax.rec_name, 'Tax Half')
            self.assertEqual(book.lines[2].taxes[2].splitline, None)
            self.assertEqual(book.lines[2].taxes[2].rec_name, 'Tax Half usd0.78 usd7.82')

            self.assertEqual(book.lines[2].amount, Decimal('10.0'))
            self.assertEqual(book.lines[2].amount_net, Decimal('7.82'))
            self.assertEqual(book.lines[2].amount_tax0, Decimal('1.40'))
            self.assertEqual(book.lines[2].amount_tax1, Decimal('0.78'))
            self.assertEqual(book.lines[2].amount_tax2, None)

            self.assertEqual(book.lines[3].rec_name, '05/04/2022|Rev/Sp|10.00 usd|Split line - one tax [-]')
            self.assertEqual(len(book.lines[3].taxes), 1)
            self.assertEqual(book.lines[3].taxes[0].amount, Decimal('0.91'))
            self.assertEqual(book.lines[3].taxes[0].base, Decimal('9.09'))
            self.assertEqual(book.lines[3].taxes[0].tax.rec_name, 'Tax Half')
            self.assertEqual(book.lines[3].taxes[0].splitline.id, book.lines[3].splitlines[0].id)
            self.assertEqual(book.lines[3].amount, Decimal('10.0'))
            self.assertEqual(book.lines[3].amount_net, None)
            self.assertEqual(book.lines[3].amount_tax0, None)
            self.assertEqual(book.lines[3].amount_tax1, None)
            self.assertEqual(book.lines[3].amount_tax2, None)
            self.assertEqual(len(book.lines[3].splitlines), 1)
            self.assertEqual(book.lines[3].splitlines[0].amount_net, Decimal('9.09'))
            self.assertEqual(book.lines[3].splitlines[0].amount_tax0, None)
            self.assertEqual(book.lines[3].splitlines[0].amount_tax1, Decimal('0.91'))
            self.assertEqual(book.lines[3].splitlines[0].amount_tax2, None)

    @with_transaction()
    def test_line_check_ena_taxes(self):
        """ create cashbook + line, check enable of fields
            at line by configured taxes on category
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Category = pool.get('cashbook.category')
        Account = pool.get('account.account')
        Journal = pool.get('account.journal')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()
        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            taxes = self.prep_line_taxes()

            accounts = Account.create([{
                'name': 'Account No 1',
                'code': '0123',
                }, {
                'name': 'Book',
                'code': '4444',
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Account No 1')
            self.assertEqual(accounts[1].rec_name, '4444 - Book')

            self.assertEqual(len(taxes), 4)
            self.assertEqual(taxes[0].rec_name, 'Tax Null')
            self.assertEqual(taxes[1].rec_name, 'Tax Half')
            self.assertEqual(taxes[2].rec_name, 'Tax Full')

            categories = Category.create([{
                'company': company.id,
                'name': 'Cat 1',
                'cattype': 'in',
                'account': taxes[1].invoice_account.id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }, {
                'company': company.id,
                'name': 'Cat 2',
                'cattype': 'in',
                'account': taxes[2].invoice_account.id,
                }])

            self.assertEqual(categories[0].rec_name, 'Cat 1 [2234]')
            self.assertEqual(categories[1].rec_name, 'Cat 2 [2235]')

            cfg1 = Configuration()
            cfg1.save()

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[1].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Text 1',
                        'category': categories[0].id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }, {
                        'date': date(2022, 6, 1),
                        'description': 'Text 2',
                        'category': categories[1].id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.name, 'Book 1')
            self.assertEqual(book.state, 'open')
            self.assertEqual(len(book.lines), 2)
            self.assertEqual(book.lines[0].avail_tax0, False)
            self.assertEqual(book.lines[0].avail_tax1, True)
            self.assertEqual(book.lines[0].avail_tax2, True)
            self.assertEqual(book.lines[1].avail_tax0, False)
            self.assertEqual(book.lines[1].avail_tax1, False)
            self.assertEqual(book.lines[1].avail_tax2, False)

    @with_transaction()
    def test_line_check_valiate_line(self):
        """ create cashbook + line, check validation of line
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Category = pool.get('cashbook.category')
        Journal = pool.get('account.journal')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            categories = Category.create([{
                'company': company.id,
                'name': 'Cat 1',
                'cattype': 'in',
                }])

            self.assertEqual(categories[0].rec_name, 'Cat 1')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Text 1',
                        'category': categories[0].id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.name, 'Book 1')
            self.assertEqual(book.state, 'open')
            self.assertEqual(len(book.lines), 1)

            self.assertRaisesRegex(UserError,
                'A value is required for field "Split booking lines" in "Cashbook Line".',
                Line.write,
                *[
                    [book.lines[0]],
                    {
                        'ena_tax1': True,
                        'bookingtype': 'spin',
                    },
                ])

    @with_transaction()
    def test_line_check_category_view_account(self):
        """ create cashbook + line, check 'category_view'
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Category = pool.get('cashbook.category')
        Account = pool.get('account.account')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        with Transaction().set_context({
            'company': company.id,
            }):
            accounts = Account.create([{
                'name': 'Account No 1',
                'code': '0123',
                }, {
                'name': 'Account No 2',
                'code': '2345',
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Account No 1')
            self.assertEqual(accounts[1].rec_name, '2345 - Account No 2')

            category2, = Category.create([{
                'company': company.id,
                'name': 'Level1',
                'cattype': 'in',
                'account': accounts[0].id,
                'childs': [('create', [{
                    'company': company.id,
                    'name': 'Level2',
                    'cattype': 'in',
                    'account': accounts[1].id,
                    }])],
                }])
            self.assertEqual(category2.rec_name, 'Level1 [0123]')
            self.assertEqual(len(category2.childs), 1)
            self.assertEqual(category2.childs[0].rec_name, 'Level1/Level2 [2345]')

            cfg1 = Configuration()
            cfg1.save()

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'lines': [('create', [{
                        'date': date(2022, 5, 1),
                        'description': 'Text 1',
                        'category': category2.id,
                        'bookingtype': 'in',
                        'amount': Decimal('1.0'),
                        'party': party.id,
                    }, {
                        'date': date(2022, 6, 1),
                        'description': 'Text 2',
                        'category': category2.childs[0].id,
                        'bookingtype': 'in',
                        'amount': Decimal('1.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.name, 'Book 1')
            self.assertEqual(book.state, 'open')
            self.assertEqual(len(book.lines), 2)

            self.assertEqual(cfg1.catnamelong, True)

            self.assertEqual(book.lines[0].category.rec_name, 'Level1 [0123]')
            self.assertEqual(book.lines[1].category.rec_name, 'Level1/Level2 [2345]')
            self.assertEqual(book.lines[0].category_view, 'Level1 [0123]')
            self.assertEqual(book.lines[1].category_view, 'Level1/Level2 [2345]')

            cfg1.catnamelong = False
            cfg1.save()
            self.assertEqual(book.lines[0].category.rec_name, 'Level1 [0123]')
            self.assertEqual(book.lines[1].category.rec_name, 'Level1/Level2 [2345]')
            self.assertEqual(book.lines[0].category_view, 'Level1 [0123]')
            self.assertEqual(book.lines[1].category_view, 'Level2 [2345]')

            cfg1.cataccno = False
            cfg1.catnamelong = True
            cfg1.save()

            self.assertEqual(book.lines[0].category.rec_name, 'Level1')
            self.assertEqual(book.lines[1].category.rec_name, 'Level1/Level2')
            self.assertEqual(book.lines[0].category_view, 'Level1')
            self.assertEqual(book.lines[1].category_view, 'Level1/Level2')

            cfg1.catnamelong = False
            cfg1.save()
            self.assertEqual(book.lines[0].category.rec_name, 'Level1')
            self.assertEqual(book.lines[1].category.rec_name, 'Level1/Level2')
            self.assertEqual(book.lines[0].category_view, 'Level1')
            self.assertEqual(book.lines[1].category_view, 'Level2')

    @with_transaction()
    def test_line_check_get_move_amounts(self):
        """ check credit/debit/2ndcurrency
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Journal = pool.get('account.journal')

        types = self.prep_type()
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        self.prep_accounting(company)
        category = self.prep_category(cattype='in')
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            books = Book.create([{
                'name': 'Book EUR',
                'btype': types.id,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': '10 €',
                        'category': category.id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }, {
                'name': 'Book USD',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': '10 USD',
                        'category': category.id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(company.currency.rec_name, 'Euro')
            self.assertEqual(len(books), 2)
            self.assertEqual(books[0].rec_name, 'Book EUR | 10.00 € | Open')
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(books[1].rec_name, 'Book USD | 10.00 usd | Open')
            self.assertEqual(len(books[1].lines), 1)

            # eur --> eur
            eur_eur_vals = Line.get_move_amounts(
                    books[0].lines[0],
                    books[0].lines[0].amount,
                )
            self.assertEqual(eur_eur_vals, {
                    'credit': Decimal('10.0'),
                    'debit': Decimal('0.0'),
                    'amount_second_currency': None,
                    'second_currency': None,
                })

            self.assertEqual(Line.get_inverted_move_values(eur_eur_vals), {
                    'credit': Decimal('00.0'),
                    'debit': Decimal('10.0'),
                    'amount_second_currency': None,
                    'second_currency': None,
                })

            # usd --> eur
            usd_eur_vals = Line.get_move_amounts(
                    books[1].lines[0],
                    books[1].lines[0].amount,
                )
            self.assertEqual(usd_eur_vals, {
                    'credit': Decimal('9.52'),
                    'debit': Decimal('0.0'),
                    'amount_second_currency': Decimal('-10.0'),
                    'second_currency': usd.id,
                })
            self.assertEqual(Line.get_inverted_move_values(usd_eur_vals), {
                    'credit': Decimal('00.0'),
                    'debit': Decimal('9.52'),
                    'amount_second_currency': Decimal('10.0'),
                    'second_currency': usd.id,
                })

    @with_transaction()
    def test_line_check_wf_in_booking_noparty(self):
        """ create cashbook + line, check booking in-type,
            company-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(moves[0].lines[1].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)

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
    def test_line_check_wf_in_booking_noparty_tax(self):
        """ create cashbook + line, check booking in-type,
            company-currency, net + tax
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        with Transaction().set_context({
            'company': company.id,
            }):
            taxes = self.prep_line_taxes()
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'tax0': taxes[0].id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')
            self.assertEqual(category2.tax0.rec_name, 'Tax Null')
            self.assertEqual(category2.tax1.rec_name, 'Tax Half')
            self.assertEqual(category2.tax2.rec_name, 'Tax Full')

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
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')
            self.assertEqual(len(book.lines[0].taxes), 0)

            # add tax
            book.lines[0].ena_tax1 = True
            book.lines[0].on_change_ena_tax1()
            book.lines[0].save()
            self.assertEqual(len(book.lines[0].taxes), 1)
            self.assertEqual(book.lines[0].taxes[0].rec_name, 'Tax Half usd0.91 usd9.09')

            # check
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')
            self.assertEqual(book.lines[0].amount, Decimal('10.0'))
            self.assertEqual(book.lines[0].ena_tax1, True)
            self.assertEqual(book.lines[0].amount_tax1, Decimal('0.91'))
            self.assertEqual(book.lines[0].amount_net, Decimal('9.09'))

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(moves[0].lines[0].rec_name, '(2234 - Tax Half)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.91'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(len(moves[0].lines[0].tax_lines), 1)
            self.assertEqual(moves[0].lines[0].tax_lines[0].amount, Decimal('0.91'))
            self.assertEqual(moves[0].lines[0].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[0].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('9.09'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(len(moves[0].lines[1].tax_lines), 1)
            self.assertEqual(moves[0].lines[1].tax_lines[0].amount, Decimal('9.09'))
            self.assertEqual(moves[0].lines[1].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[1].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)

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
    def test_line_check_wf_in_split_booking_noparty(self):
        """ create cashbook + line, check booking in-type,
            company-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'sell something',
                        'bookingtype': 'spin',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')
            self.assertEqual(moves[0].lines[0].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].description, 'line 1')
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party, None)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].description, 'line 2')
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].origin, None)

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
    def test_line_check_wf_in_split_booking_noparty_transfer(self):
        """ create cashbook + line, check booking in-type,
            company-currency, transfer with fee
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

            accounts = Account.create([{
                'name': 'Account Book 1',
                'code': '0123',
                'type': acc_type.id,
                }, {
                'name': 'Account Book 2',
                'code': '3456',
                'type': acc_type.id,
                }, {
                'name': 'Account Category',
                'code': '2345',
                'type': acc_type.id,
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Account Book 1')
            self.assertEqual(accounts[0].type.currency.code, 'usd')
            self.assertEqual(accounts[1].rec_name, '3456 - Account Book 2')
            self.assertEqual(accounts[1].type.currency.code, 'usd')
            self.assertEqual(accounts[2].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[2].type.currency.code, 'usd')
            self.assertEqual(company.currency.code, 'usd')

            category2, = Category.create([{
                'company': company.id,
                'name': 'In-Category',
                'cattype': 'in',
                'account': accounts[2].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')

            books = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }, {
                'name': 'Book 2',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[1].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }])
            self.assertEqual(books[0].rec_name, 'Book 1 | 0.00 usd | Open')
            self.assertEqual(books[0].account.rec_name, '0123 - Account Book 1')
            self.assertEqual(len(books[0].lines), 0)
            self.assertEqual(books[1].rec_name, 'Book 2 | 0.00 usd | Open')
            self.assertEqual(books[1].account.rec_name, '3456 - Account Book 2')
            self.assertEqual(len(books[1].lines), 0)

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'transfer with fee',
                        'bookingtype': 'spin',
                        'amount': Decimal('30.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                                'splittype': 'cat',
                                'amount': Decimal('5.0'),
                                'category': category2.id,
                                'description': 'fee for transfer',
                            }, {
                                'splittype': 'tr',
                                'amount': Decimal('25.0'),
                                'booktransf': books[1].id,
                                'description': 'transfer amount',
                            }])],
                        }])],
                }])
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(len(books[1].lines), 0)

            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')
            self.assertEqual(len(books[0].lines[0].moves), 0)
            self.assertEqual(books[0].lines[0].category, None)
            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(books[0].lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|fee for transfer [In-Category [2345]]')
            self.assertEqual(books[0].lines[0].splitlines[1].rec_name, \
                'Rev/Sp|25.00 usd|transfer amount [Book 2 | 0.00 usd | Open]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([books[0].lines[0]])

            # check book 1
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].category, None)
            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(books[0].lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|fee for transfer [In-Category [2345]]')
            self.assertEqual(books[0].lines[0].splitlines[1].rec_name, \
                'Rev/Sp|25.00 usd|transfer amount [Book 2 | -25.00 usd | Open]')

            # check book 2
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(books[1].lines[0].rec_name,
                '05/05/2022|to|-25.00 usd|transfer amount [Book 1 | 30.00 usd | Open]')
            self.assertEqual(len(books[1].lines[0].moves), 0)
            self.assertEqual(books[1].lines[0].reference.rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'transfer with fee')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')
            self.assertEqual(moves[0].lines[0].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].description, 'fee for transfer')
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party, None)
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                'Rev/Sp|5.00 usd|fee for transfer [In-Category [2345]]')

            self.assertEqual(moves[0].lines[1].rec_name, '(3456 - Account Book 2)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('25.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].description, 'transfer amount')
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Rev/Sp|25.00 usd|transfer amount [Book 2 | -25.00 usd | Open]')

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book 1')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('30.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin, None)

            # delete move
            Line.wfedit([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 0)

            # create move again
            Line.wfcheck([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'draft')

            # post move
            Line.wfdone([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'posted')

    @with_transaction()
    def test_line_check_wf_in_booking_withparty(self):
        """ create cashbook + line, check booking in-type,
            company-currency, include party-accounts
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'party_account': True,
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
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 4)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(moves[0].lines[0].rec_name, 'Main Receivable')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party.rec_name, 'Party')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin, None)

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin, None)

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin, None)

            self.assertEqual(moves[0].lines[3].rec_name, '(Main Receivable)')
            self.assertEqual(moves[0].lines[3].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, None)
            self.assertEqual(moves[0].lines[3].party.rec_name, 'Party')
            self.assertEqual(len(moves[0].lines[3].tax_lines), 0)
            self.assertEqual(moves[0].lines[3].origin, None)

            # delete move
            Line.wfedit([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 0)

            # create move again
            Line.wfcheck([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'draft')

            # post move
            self.assertEqual(Reconciliation.search_count([]), 0)
            Line.wfdone([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'posted')

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_in_booking_withparty_tax(self):
        """ create cashbook + line, check booking in-type,
            company-currency, include party-accounts
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            taxes = self.prep_line_taxes()
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'tax0': taxes[0].id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')
            self.assertEqual(category2.tax0.rec_name, 'Tax Null')
            self.assertEqual(category2.tax1.rec_name, 'Tax Half')
            self.assertEqual(category2.tax2.rec_name, 'Tax Full')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'sell something',
                        'category': category2.id,
                        'bookingtype': 'in',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'ena_tax1': True,
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')
            self.assertEqual(len(book.lines[0].taxes), 1)
            self.assertEqual(book.lines[0].taxes[0].rec_name, 'Tax Half usd0.91 usd9.09')
            self.assertEqual(book.lines[0].amount, Decimal('10.0'))
            self.assertEqual(book.lines[0].ena_tax1, True)
            self.assertEqual(book.lines[0].amount_tax1, Decimal('0.91'))
            self.assertEqual(book.lines[0].amount_net, Decimal('9.09'))

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 5)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')

            self.assertEqual(moves[0].lines[0].rec_name, 'Main Receivable')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[0].origin, None)
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)

            self.assertEqual(moves[0].lines[1].rec_name, '(2234 - Tax Half)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.91'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].origin, None)
            self.assertEqual(len(moves[0].lines[1].tax_lines), 1)
            self.assertEqual(moves[0].lines[1].tax_lines[0].amount, Decimal('0.91'))
            self.assertEqual(moves[0].lines[1].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[1].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[2].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('9.09'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].origin, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 1)
            self.assertEqual(moves[0].lines[2].tax_lines[0].amount, Decimal('9.09'))
            self.assertEqual(moves[0].lines[2].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[2].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[3].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[3].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, None)
            self.assertEqual(moves[0].lines[3].party, None)
            self.assertEqual(len(moves[0].lines[3].tax_lines), 0)
            self.assertEqual(moves[0].lines[3].origin, None)

            self.assertEqual(moves[0].lines[4].rec_name, '(Main Receivable)')
            self.assertEqual(moves[0].lines[4].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[4].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[4].amount_second_currency, None)
            self.assertEqual(moves[0].lines[4].party.rec_name, 'Party')
            self.assertEqual(len(moves[0].lines[4].tax_lines), 0)
            self.assertEqual(moves[0].lines[4].origin, None)

            # delete move
            Line.wfedit([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 0)

            # create move again
            Line.wfcheck([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'draft')

            # post move
            self.assertEqual(Reconciliation.search_count([]), 0)
            Line.wfdone([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'posted')

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_in_split_booking_withparty(self):
        """ create cashbook + line, check booking in-type,
            company-currency, include party-accounts
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'sell something',
                        'bookingtype': 'spin',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 5)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')
            self.assertEqual(moves[0].lines[0].rec_name, 'Main Receivable')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party.rec_name, 'Party')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 1')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')

            self.assertEqual(moves[0].lines[2].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, 'line 2')
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin.rec_name,
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(moves[0].lines[3].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[3].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, None)
            self.assertEqual(moves[0].lines[3].party, None)
            self.assertEqual(len(moves[0].lines[3].tax_lines), 0)
            self.assertEqual(moves[0].lines[3].origin, None)

            self.assertEqual(moves[0].lines[4].rec_name, '(Main Receivable)')
            self.assertEqual(moves[0].lines[4].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[4].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[4].amount_second_currency, None)
            self.assertEqual(moves[0].lines[4].party.rec_name, 'Party')
            self.assertEqual(len(moves[0].lines[4].tax_lines), 0)
            self.assertEqual(moves[0].lines[4].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')

            # delete move
            Line.wfedit([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 0)

            # create move again
            Line.wfcheck([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'draft')

            # post move
            self.assertEqual(Reconciliation.search_count([]), 0)
            Line.wfdone([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'posted')

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_in_split_booking_withparty_tax(self):
        """ create cashbook + line, check booking in-type,
            company-currency, include party-accounts
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            taxes = self.prep_line_taxes()
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'tax0': taxes[0].id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')
            self.assertEqual(category2.tax0.rec_name, 'Tax Null')
            self.assertEqual(category2.tax1.rec_name, 'Tax Half')
            self.assertEqual(category2.tax2.rec_name, 'Tax Full')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'sell something',
                        'bookingtype': 'spin',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            'ena_tax1': True,
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            'ena_tax2': True,
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(len(book.lines[0].taxes), 2)
            self.assertEqual(book.lines[0].taxes[0].amount, Decimal('0.83'))
            self.assertEqual(book.lines[0].taxes[0].base, Decimal('4.17'))
            self.assertEqual(book.lines[0].taxes[0].tax.rec_name, 'Tax Full')
            self.assertEqual(book.lines[0].taxes[0].splitline.rec_name,
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')
            self.assertEqual(book.lines[0].taxes[1].amount, Decimal('0.46'))
            self.assertEqual(book.lines[0].taxes[1].base, Decimal('4.54'))
            self.assertEqual(book.lines[0].taxes[1].tax.rec_name, 'Tax Half')
            self.assertEqual(book.lines[0].taxes[1].splitline.rec_name,
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 7)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')

            self.assertEqual(moves[0].lines[0].rec_name, 'Main Receivable')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party.rec_name, 'Party')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('4.54'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 1')
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')
            self.assertEqual(moves[0].lines[1].tax_lines[0].amount, Decimal('4.54'))
            self.assertEqual(moves[0].lines[1].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[1].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[2].rec_name, '(2234 - Tax Half)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.46'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, 'line 1')
            self.assertEqual(moves[0].lines[2].origin.rec_name,
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')
            self.assertEqual(len(moves[0].lines[2].tax_lines), 1)
            self.assertEqual(moves[0].lines[2].tax_lines[0].amount, Decimal('0.46'))
            self.assertEqual(moves[0].lines[2].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[2].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[3].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[3].credit, Decimal('4.17'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, None)
            self.assertEqual(moves[0].lines[3].party, None)
            self.assertEqual(moves[0].lines[3].description, 'line 2')
            self.assertEqual(moves[0].lines[3].origin.rec_name,
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')
            self.assertEqual(len(moves[0].lines[3].tax_lines), 1)
            self.assertEqual(moves[0].lines[3].tax_lines[0].amount, Decimal('4.17'))
            self.assertEqual(moves[0].lines[3].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[3].tax_lines[0].tax.rec_name, 'Tax Full')

            self.assertEqual(moves[0].lines[4].rec_name, '(2235 - Tax Full)')
            self.assertEqual(moves[0].lines[4].credit, Decimal('0.83'))
            self.assertEqual(moves[0].lines[4].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[4].amount_second_currency, None)
            self.assertEqual(moves[0].lines[4].party, None)
            self.assertEqual(moves[0].lines[4].description, 'line 2')
            self.assertEqual(moves[0].lines[4].origin.rec_name,
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')
            self.assertEqual(len(moves[0].lines[4].tax_lines), 1)
            self.assertEqual(moves[0].lines[4].tax_lines[0].amount, Decimal('0.83'))
            self.assertEqual(moves[0].lines[4].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[4].tax_lines[0].tax.rec_name, 'Tax Full')

            self.assertEqual(moves[0].lines[5].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[5].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[5].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[5].amount_second_currency, None)
            self.assertEqual(moves[0].lines[5].party, None)
            self.assertEqual(len(moves[0].lines[5].tax_lines), 0)
            self.assertEqual(moves[0].lines[5].origin, None)

            self.assertEqual(moves[0].lines[6].rec_name, '(Main Receivable)')
            self.assertEqual(moves[0].lines[6].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[6].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[6].amount_second_currency, None)
            self.assertEqual(moves[0].lines[6].party.rec_name, 'Party')
            self.assertEqual(len(moves[0].lines[6].tax_lines), 0)
            self.assertEqual(moves[0].lines[6].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')

            # delete move
            Line.wfedit([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 0)

            # create move again
            Line.wfcheck([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'draft')

            # post move
            self.assertEqual(Reconciliation.search_count([]), 0)
            Line.wfdone([book.lines[0]])
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(book.lines[0].moves[0].state, 'posted')

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_in_booking_2nd_currency_noparty(self):
        """ create cashbook + line, check booking in-type,
            2nd-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

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
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
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
            self.assertEqual(book.currency.code, 'usd')
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
            self.assertEqual(moves[0].lines[0].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')

            self.assertEqual(moves[0].lines[1].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')

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
    def test_line_check_wf_in_booking_2nd_currency_noparty_tax(self):
        """ create cashbook + line, check booking in-type,
            2nd-currency, net + tax
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            taxes = self.prep_line_taxes()
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            category2, = Category.create([{
                'company': company.id,
                'name': 'In-Category',
                'cattype': 'in',
                'account': accounts[1].id,
                'tax0': taxes[0].id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')
            self.assertEqual(category2.tax0.rec_name, 'Tax Null')
            self.assertEqual(category2.tax1.rec_name, 'Tax Half')
            self.assertEqual(category2.tax2.rec_name, 'Tax Full')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
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
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')

            # add tax
            book.lines[0].ena_tax1 = True
            book.lines[0].on_change_ena_tax1()
            book.lines[0].save()

            # check
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')
            self.assertEqual(book.lines[0].currency.rec_name, 'usd')
            self.assertEqual(book.lines[0].amount, Decimal('10.0'))
            self.assertEqual(book.lines[0].ena_tax1, True)
            self.assertEqual(book.lines[0].amount_tax1, Decimal('0.91'))
            self.assertEqual(book.lines[0].amount_net, Decimal('9.09'))

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')

            self.assertEqual(moves[0].lines[0].rec_name, '(2234 - Tax Half)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.86'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('-0.91'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 1)
            self.assertEqual(moves[0].lines[0].tax_lines[0].amount, Decimal('0.86'))
            self.assertEqual(moves[0].lines[0].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[0].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('8.66'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('-9.09'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 1)
            self.assertEqual(moves[0].lines[1].tax_lines[0].amount, Decimal('8.66'))
            self.assertEqual(moves[0].lines[1].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[1].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)

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
    def test_line_check_wf_in_split_booking_2nd_currency_noparty(self):
        """ create cashbook + line, check booking in-type,
            2nd-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

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
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'sell something',
                        'bookingtype': 'spin',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')
            self.assertEqual(moves[0].lines[0].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('-5.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[0].party, None)
            self.assertEqual(moves[0].lines[0].description, 'line 1')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('-5.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 2')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin, None)

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
    def test_line_check_wf_in_split_booking_2nd_currency_transfer(self):
        """ create cashbook + line, check booking in-type,
            2nd-currency, transfer with fee,
            company-currency: eur, 2x account-currency: usd
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

            accounts = Account.create([{
                'name': 'Account Book 1',
                'code': '0123',
                'type': acc_type.id,
                }, {
                'name': 'Account Book 2',
                'code': '3456',
                'type': acc_type.id,
                }, {
                'name': 'Account Category',
                'code': '2345',
                'type': acc_type.id,
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Account Book 1')
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '3456 - Account Book 2')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(accounts[2].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[2].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            category2, = Category.create([{
                'company': company.id,
                'name': 'In-Category',
                'cattype': 'in',
                'account': accounts[2].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')

            books = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }, {
                'name': 'Book 2',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[1].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }])
            self.assertEqual(books[0].rec_name, 'Book 1 | 0.00 usd | Open')
            self.assertEqual(books[0].account.rec_name, '0123 - Account Book 1')
            self.assertEqual(books[0].currency.code, 'usd')
            self.assertEqual(len(books[0].lines), 0)
            self.assertEqual(books[1].rec_name, 'Book 2 | 0.00 usd | Open')
            self.assertEqual(books[1].account.rec_name, '3456 - Account Book 2')
            self.assertEqual(books[1].currency.code, 'usd')
            self.assertEqual(len(books[1].lines), 0)

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'transfer with fee',
                        'bookingtype': 'spin',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'splittype': 'cat',
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'fee',
                            }, {
                            'splittype': 'tr',
                            'amount': Decimal('25.0'),
                            'booktransf': books[1].id,
                            'description': 'transfer',
                            }])],
                    }])],
                }])
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(len(books[1].lines), 0)

            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')
            self.assertEqual(len(books[0].lines[0].moves), 0)
            self.assertEqual(books[0].lines[0].category, None)
            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(books[0].lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|fee [In-Category [2345]]')
            self.assertEqual(books[0].lines[0].splitlines[1].rec_name, \
                'Rev/Sp|25.00 usd|transfer [Book 2 | 0.00 usd | Open]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([books[0].lines[0]])

            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(books[1].lines[0].rec_name,
                '05/05/2022|to|-25.00 usd|transfer [Book 1 | 30.00 usd | Open]')
            self.assertEqual(len(books[1].lines[0].moves), 0)
            self.assertEqual(books[1].lines[0].reference.rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'transfer with fee')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')
            self.assertEqual(moves[0].lines[0].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('-5.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[0].party, None)
            self.assertEqual(moves[0].lines[0].description, 'fee')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                'Rev/Sp|5.00 usd|fee [In-Category [2345]]')

            self.assertEqual(moves[0].lines[1].rec_name, '(3456 - Account Book 2)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('23.81'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('-25.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'transfer')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Rev/Sp|25.00 usd|transfer [Book 2 | -25.00 usd | Open]')

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book 1')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('28.57'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('30.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin, None)

            # delete move
            Line.wfedit([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 0)

            # create move again
            Line.wfcheck([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'draft')

            # post move
            Line.wfdone([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'posted')

    @with_transaction()
    def test_line_check_wf_in_split_booking_2nd_currency_transfer2(self):
        """ create cashbook + line, check booking in-type,
            2nd-currency, transfer with fee,
            company-currency: eur,
            1x account-currency: usd
            1x account-currency: eur
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

            accounts = Account.create([{
                'name': 'Account Book 1',
                'code': '0123',
                'type': acc_type.id,
                }, {
                'name': 'Account Book 2',
                'code': '3456',
                'type': acc_type.id,
                }, {
                'name': 'Account Category',
                'code': '2345',
                'type': acc_type.id,
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Account Book 1')
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '3456 - Account Book 2')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(accounts[2].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[2].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            category2, = Category.create([{
                'company': company.id,
                'name': 'In-Category',
                'cattype': 'in',
                'account': accounts[2].id,
                }])
            self.assertEqual(category2.rec_name, 'In-Category [2345]')

            books = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }, {
                'name': 'Book 2',
                'btype': types.id,
                'company': company.id,
                'currency': euro.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[1].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }])
            self.assertEqual(books[0].rec_name, 'Book 1 | 0.00 usd | Open')
            self.assertEqual(books[0].account.rec_name, '0123 - Account Book 1')
            self.assertEqual(books[0].currency.code, 'usd')
            self.assertEqual(len(books[0].lines), 0)
            self.assertEqual(books[1].rec_name, 'Book 2 | 0.00 € | Open')
            self.assertEqual(books[1].account.rec_name, '3456 - Account Book 2')
            self.assertEqual(books[1].currency.code, 'EUR')
            self.assertEqual(len(books[1].lines), 0)

            Book.write(*[
                [books[0]],
                {
                    'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'transfer with fee',
                        'bookingtype': 'spin',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'splittype': 'cat',
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'fee',
                            }, {
                            'splittype': 'tr',
                            'amount': Decimal('25.0'),
                            'booktransf': books[1].id,
                            'description': 'transfer',
                            }])],
                    }])],
                }])
            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(len(books[1].lines), 0)

            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')
            self.assertEqual(len(books[0].lines[0].moves), 0)
            self.assertEqual(books[0].lines[0].category, None)
            self.assertEqual(len(books[0].lines[0].splitlines), 2)
            self.assertEqual(books[0].lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|fee [In-Category [2345]]')
            self.assertEqual(books[0].lines[0].splitlines[1].rec_name, \
                'Rev/Sp|25.00 usd|transfer [Book 2 | 0.00 € | Open]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([books[0].lines[0]])

            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(books[1].lines[0].rec_name,
                '05/05/2022|to|-23.81 €|transfer [Book 1 | 30.00 usd | Open]')
            self.assertEqual(len(books[1].lines[0].moves), 0)
            self.assertEqual(books[1].lines[0].reference.rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'transfer with fee')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev/Sp|30.00 usd|transfer with fee [-]')
            self.assertEqual(moves[0].lines[0].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('-5.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[0].party, None)
            self.assertEqual(moves[0].lines[0].description, 'fee')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                'Rev/Sp|5.00 usd|fee [In-Category [2345]]')

            self.assertEqual(moves[0].lines[1].rec_name, '(3456 - Account Book 2)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('23.81'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('-25.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'transfer')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Rev/Sp|25.00 usd|transfer [Book 2 | -23.81 € | Open]')

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book 1')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('28.57'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('30.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin, None)

            # delete move
            Line.wfedit([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 0)

            # create move again
            Line.wfcheck([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'draft')

            # post move
            Line.wfdone([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'posted')

    @with_transaction()
    def test_line_check_wf_in_booking_2nd_currency_withparty(self):
        """ create cashbook + line, check booking in-type,
            2nd-currency
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

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
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
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
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'In-Category [2345]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 4)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev|10.00 usd|sell something [In-Category [2345]]')

            self.assertEqual(moves[0].lines[0].rec_name, 'Main Receivable')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')

            self.assertEqual(moves[0].lines[2].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')

            self.assertEqual(moves[0].lines[3].rec_name, '(Main Receivable)')
            self.assertEqual(moves[0].lines[3].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[3].second_currency.rec_name, 'usd')

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

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_in_split_booking_2nd_currency_withparty(self):
        """ create cashbook + line, check booking in-type,
            2nd-currency
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

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
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'sell something',
                        'bookingtype': 'spin',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | 10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 5)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'sell something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')

            self.assertEqual(moves[0].lines[0].rec_name, 'Main Receivable')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[0].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[0].description, None)
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')

            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('-5.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 1')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Rev/Sp|5.00 usd|line 1 [In-Category [2345]]')

            self.assertEqual(moves[0].lines[2].rec_name, '(2345 - Account Category)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('-5.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, 'line 2')
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin.rec_name,
                'Rev/Sp|5.00 usd|line 2 [In-Category [2345]]')

            self.assertEqual(moves[0].lines[3].rec_name, '0123 - Account Book')
            self.assertEqual(moves[0].lines[3].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[3].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[3].party, None)
            self.assertEqual(moves[0].lines[3].description, None)
            self.assertEqual(len(moves[0].lines[3].tax_lines), 0)
            self.assertEqual(moves[0].lines[3].origin, None)

            self.assertEqual(moves[0].lines[4].rec_name, '(Main Receivable)')
            self.assertEqual(moves[0].lines[4].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[4].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[4].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[4].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[4].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[4].description, None)
            self.assertEqual(len(moves[0].lines[4].tax_lines), 0)
            self.assertEqual(moves[0].lines[4].origin.rec_name,
                '05/05/2022|Rev/Sp|10.00 usd|sell something [-]')

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

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_out_booking_noparty(self):
        """ create cashbook + line, check booking out-type,
            company-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')

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
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'category': category2.id,
                        'bookingtype': 'out',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'Out-Category [2345]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 2)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')
            self.assertEqual(moves[0].lines[0].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)

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
    def test_line_check_wf_out_booking_noparty_tax(self):
        """ create cashbook + line, check booking out-type,
            company-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            taxes = self.prep_line_taxes()
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                'tax0': taxes[0].id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')
            self.assertEqual(category2.tax0.rec_name, 'Tax Null')
            self.assertEqual(category2.tax1.rec_name, 'Tax Half')
            self.assertEqual(category2.tax2.rec_name, 'Tax Full')

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
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'category': category2.id,
                        'bookingtype': 'out',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'ena_tax1': True,
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'Out-Category [2345]')
            self.assertEqual(book.lines[0].amount, Decimal('10.0'))
            self.assertEqual(book.lines[0].ena_tax1, True)
            self.assertEqual(book.lines[0].amount_tax1, Decimal('0.91'))
            self.assertEqual(book.lines[0].amount_net, Decimal('9.09'))
            self.assertEqual(len(book.lines[0].taxes), 1)
            self.assertEqual(book.lines[0].taxes[0].rec_name, 'Tax Half usd0.91 usd9.09')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')

            self.assertEqual(moves[0].lines[0].rec_name, '2234 - Tax Half')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.91'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].origin, None)
            self.assertEqual(len(moves[0].lines[0].tax_lines), 1)
            self.assertEqual(moves[0].lines[0].tax_lines[0].amount, Decimal('0.91'))
            self.assertEqual(moves[0].lines[0].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[0].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('9.09'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].origin, None)
            self.assertEqual(len(moves[0].lines[1].tax_lines), 1)
            self.assertEqual(moves[0].lines[1].tax_lines[0].amount, Decimal('9.09'))
            self.assertEqual(moves[0].lines[1].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[1].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[2].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].origin, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)

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
    def test_line_check_wf_out_split_booking_noparty(self):
        """ create cashbook + line, check booking out-type,
            company-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')

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
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'bookingtype': 'spout',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')

            self.assertEqual(moves[0].lines[0].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party, None)
            self.assertEqual(moves[0].lines[0].description, 'line 1')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 2')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')

            self.assertEqual(moves[0].lines[2].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin, None)

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
    def test_line_check_wf_out_booking_withparty(self):
        """ create cashbook + line, check booking out-type,
            company-currency
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'category': category2.id,
                        'bookingtype': 'out',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'Out-Category [2345]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 4)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')

            self.assertEqual(moves[0].lines[0].rec_name, '(Main Payable)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('00.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)

            self.assertEqual(moves[0].lines[2].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)

            self.assertEqual(moves[0].lines[3].rec_name, 'Main Payable')
            self.assertEqual(moves[0].lines[3].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, None)

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

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_out_split_booking_withparty(self):
        """ create cashbook + line, check booking out-type,
            company-currency
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'bookingtype': 'spout',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 5)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')

            self.assertEqual(moves[0].lines[0].rec_name, '(Main Payable)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('00.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[0].description, None)
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 1')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')

            self.assertEqual(moves[0].lines[2].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('5.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, 'line 2')
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)
            self.assertEqual(moves[0].lines[2].origin.rec_name,
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')

            self.assertEqual(moves[0].lines[3].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[3].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, None)
            self.assertEqual(moves[0].lines[3].party, None)
            self.assertEqual(moves[0].lines[3].description, None)
            self.assertEqual(len(moves[0].lines[3].tax_lines), 0)
            self.assertEqual(moves[0].lines[3].origin, None)

            self.assertEqual(moves[0].lines[4].rec_name, 'Main Payable')
            self.assertEqual(moves[0].lines[4].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[4].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[4].amount_second_currency, None)
            self.assertEqual(moves[0].lines[4].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[4].description, None)
            self.assertEqual(len(moves[0].lines[4].tax_lines), 0)
            self.assertEqual(moves[0].lines[4].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')

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

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_out_split_booking_withparty_tax(self):
        """ create cashbook + line, check booking out-type,
            company-currency
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            taxes = self.prep_line_taxes()
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                'tax0': taxes[0].id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')
            self.assertEqual(category2.tax0.rec_name, 'Tax Null')
            self.assertEqual(category2.tax1.rec_name, 'Tax Half')
            self.assertEqual(category2.tax2.rec_name, 'Tax Full')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'bookingtype': 'spout',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            'ena_tax1': True,
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            'ena_tax2': True,
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')

            self.assertEqual(len(book.lines[0].taxes), 2)
            self.assertEqual(book.lines[0].taxes[0].rec_name, 'Tax Full usd0.83 usd4.17')
            self.assertEqual(book.lines[0].taxes[0].amount, Decimal('0.83'))
            self.assertEqual(book.lines[0].taxes[0].base, Decimal('4.17'))
            self.assertEqual(book.lines[0].taxes[0].tax.rec_name, 'Tax Full')
            self.assertEqual(book.lines[0].taxes[0].splitline.rec_name,
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')
            self.assertEqual(book.lines[0].taxes[1].rec_name, 'Tax Half usd0.46 usd4.54')
            self.assertEqual(book.lines[0].taxes[1].amount, Decimal('0.46'))
            self.assertEqual(book.lines[0].taxes[1].base, Decimal('4.54'))
            self.assertEqual(book.lines[0].taxes[1].tax.rec_name, 'Tax Half')
            self.assertEqual(book.lines[0].taxes[1].splitline.rec_name,
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 7)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')

            self.assertEqual(moves[0].lines[0].rec_name, '(Main Payable)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('00.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[0].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[0].description, None)
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('4.54'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 1')
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 1)
            self.assertEqual(moves[0].lines[1].tax_lines[0].amount, Decimal('4.54'))
            self.assertEqual(moves[0].lines[1].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[1].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[2].rec_name, '2234 - Tax Half')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.46'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, None)
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, 'line 1')
            self.assertEqual(moves[0].lines[2].origin.rec_name,
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(len(moves[0].lines[2].tax_lines), 1)
            self.assertEqual(moves[0].lines[2].tax_lines[0].amount, Decimal('0.46'))
            self.assertEqual(moves[0].lines[2].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[2].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[3].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[3].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('4.17'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, None)
            self.assertEqual(moves[0].lines[3].party, None)
            self.assertEqual(moves[0].lines[3].description, 'line 2')
            self.assertEqual(moves[0].lines[3].origin.rec_name,
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')
            self.assertEqual(len(moves[0].lines[3].tax_lines), 1)
            self.assertEqual(moves[0].lines[3].tax_lines[0].amount, Decimal('4.17'))
            self.assertEqual(moves[0].lines[3].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[3].tax_lines[0].tax.rec_name, 'Tax Full')

            self.assertEqual(moves[0].lines[4].rec_name, '2235 - Tax Full')
            self.assertEqual(moves[0].lines[4].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[4].debit, Decimal('0.83'))
            self.assertEqual(moves[0].lines[4].amount_second_currency, None)
            self.assertEqual(moves[0].lines[4].party, None)
            self.assertEqual(moves[0].lines[4].description, 'line 2')
            self.assertEqual(moves[0].lines[4].origin.rec_name,
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')
            self.assertEqual(len(moves[0].lines[4].tax_lines), 1)
            self.assertEqual(moves[0].lines[4].tax_lines[0].amount, Decimal('0.83'))
            self.assertEqual(moves[0].lines[4].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[4].tax_lines[0].tax.rec_name, 'Tax Full')

            self.assertEqual(moves[0].lines[5].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[5].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[5].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[5].amount_second_currency, None)
            self.assertEqual(moves[0].lines[5].party, None)
            self.assertEqual(moves[0].lines[5].description, None)
            self.assertEqual(moves[0].lines[5].origin, None)
            self.assertEqual(len(moves[0].lines[5].tax_lines), 0)

            self.assertEqual(moves[0].lines[6].rec_name, 'Main Payable')
            self.assertEqual(moves[0].lines[6].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[6].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[6].amount_second_currency, None)
            self.assertEqual(moves[0].lines[6].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[6].description, None)
            self.assertEqual(moves[0].lines[6].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')
            self.assertEqual(len(moves[0].lines[6].tax_lines), 0)

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

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_out_booking_2nd_currency_noparty(self):
        """ create cashbook + line, check booking out-type,
            2nd-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            category2, = Category.create([{
                'company': company.id,
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'category': category2.id,
                        'bookingtype': 'out',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'Out-Category [2345]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 2)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')
            self.assertEqual(moves[0].lines[0].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[1].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')

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
    def test_line_check_wf_out_booking_2nd_currency_noparty_tax(self):
        """ create cashbook + line, check booking out-type,
            2nd-currency, with tax
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            taxes = self.prep_line_taxes()
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            category2, = Category.create([{
                'company': company.id,
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                'tax0': taxes[0].id,
                'tax1': taxes[1].id,
                'tax2': taxes[2].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')
            self.assertEqual(category2.tax0.rec_name, 'Tax Null')
            self.assertEqual(category2.tax1.rec_name, 'Tax Half')
            self.assertEqual(category2.tax2.rec_name, 'Tax Full')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'category': category2.id,
                        'bookingtype': 'out',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'ena_tax1': True
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'Out-Category [2345]')
            self.assertEqual(len(book.lines[0].taxes), 1)
            self.assertEqual(book.lines[0].taxes[0].rec_name, 'Tax Half usd0.91 usd9.09')
            self.assertEqual(book.lines[0].amount, Decimal('10.0'))
            self.assertEqual(book.lines[0].ena_tax1, True)
            self.assertEqual(book.lines[0].amount_tax1, Decimal('0.91'))
            self.assertEqual(book.lines[0].amount_net, Decimal('9.09'))

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')

            self.assertEqual(moves[0].lines[0].rec_name, '2234 - Tax Half')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.86'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('0.91'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 1)
            self.assertEqual(moves[0].lines[0].tax_lines[0].amount, Decimal('0.86'))
            self.assertEqual(moves[0].lines[0].tax_lines[0].type, 'tax')
            self.assertEqual(moves[0].lines[0].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('8.66'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('9.09'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 1)
            self.assertEqual(moves[0].lines[1].tax_lines[0].amount, Decimal('8.66'))
            self.assertEqual(moves[0].lines[1].tax_lines[0].type, 'base')
            self.assertEqual(moves[0].lines[1].tax_lines[0].tax.rec_name, 'Tax Half')

            self.assertEqual(moves[0].lines[2].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)

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
    def test_line_check_wf_out_split_booking_2nd_currency_noparty(self):
        """ create cashbook + line, check booking out-type,
            2nd-currency
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

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            category2, = Category.create([{
                'company': company.id,
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'bookingtype': 'spout',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 3)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')

            self.assertEqual(moves[0].lines[0].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('5.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[0].party, None)
            self.assertEqual(moves[0].lines[0].description, 'line 1')
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('5.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 2')
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)

            self.assertEqual(moves[0].lines[2].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, None)
            self.assertEqual(moves[0].lines[2].origin, None)
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)

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
    def test_line_check_wf_out_booking_2nd_currency_withparty(self):
        """ create cashbook + line, check booking out-type,
            2nd-currency
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            category2, = Category.create([{
                'company': company.id,
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'category': category2.id,
                        'bookingtype': 'out',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category.rec_name, 'Out-Category [2345]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 4)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp|-10.00 usd|buy something [Out-Category [2345]]')

            self.assertEqual(moves[0].lines[0].rec_name, '(Main Payable)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')

            self.assertEqual(moves[0].lines[2].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[2].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')

            self.assertEqual(moves[0].lines[3].rec_name, 'Main Payable')
            self.assertEqual(moves[0].lines[3].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[3].second_currency.rec_name, 'usd')

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

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_out_split_booking_2nd_currency_withparty(self):
        """ create cashbook + line, check booking out-type,
            2nd-currency
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
        Reconciliation = pool.get('account.move.reconciliation')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

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
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Account Category')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            category2, = Category.create([{
                'company': company.id,
                'name': 'Out-Category',
                'cattype': 'out',
                'account': accounts[1].id,
                }])
            self.assertEqual(category2.rec_name, 'Out-Category [2345]')

            book, = Book.create([{
                'name': 'Book 1',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': True,
                'lines': [('create', [{
                        'date': date(2022, 5, 5),
                        'description': 'buy something',
                        'bookingtype': 'spout',
                        'amount': Decimal('10.0'),
                        'party': party.id,
                        'splitlines': [('create', [{
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 1',
                            }, {
                            'amount': Decimal('5.0'),
                            'category': category2.id,
                            'description': 'line 2',
                            }])],
                    }])],
                }])
            self.assertEqual(book.rec_name, 'Book 1 | -10.00 usd | Open')
            self.assertEqual(book.account.rec_name, '0123 - Account Book')
            self.assertEqual(book.currency.code, 'usd')
            self.assertEqual(len(book.lines), 1)
            self.assertEqual(book.lines[0].rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')
            self.assertEqual(len(book.lines[0].moves), 0)
            self.assertEqual(book.lines[0].category, None)
            self.assertEqual(len(book.lines[0].splitlines), 2)
            self.assertEqual(book.lines[0].splitlines[0].rec_name, \
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(book.lines[0].splitlines[1].rec_name, \
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')

            self.assertEqual(Move.search_count([]), 0)
            Line.wfcheck([book.lines[0]])

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 5)
            self.assertEqual(len(book.lines[0].moves), 1)
            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'buy something')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')

            self.assertEqual(moves[0].lines[0].rec_name, '(Main Payable)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[0].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[0].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[0].description, None)
            self.assertEqual(moves[0].lines[0].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')
            self.assertEqual(len(moves[0].lines[0].tax_lines), 0)

            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, Decimal('5.0'))
            self.assertEqual(moves[0].lines[1].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[1].party, None)
            self.assertEqual(moves[0].lines[1].description, 'line 1')
            self.assertEqual(moves[0].lines[1].origin.rec_name,
                'Exp/Sp|5.00 usd|line 1 [Out-Category [2345]]')
            self.assertEqual(len(moves[0].lines[1].tax_lines), 0)

            self.assertEqual(moves[0].lines[2].rec_name, '2345 - Account Category')
            self.assertEqual(moves[0].lines[2].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[2].debit, Decimal('4.76'))
            self.assertEqual(moves[0].lines[2].amount_second_currency, Decimal('5.0'))
            self.assertEqual(moves[0].lines[2].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[2].party, None)
            self.assertEqual(moves[0].lines[2].description, 'line 2')
            self.assertEqual(moves[0].lines[2].origin.rec_name,
                'Exp/Sp|5.00 usd|line 2 [Out-Category [2345]]')
            self.assertEqual(len(moves[0].lines[2].tax_lines), 0)

            self.assertEqual(moves[0].lines[3].rec_name, '(0123 - Account Book)')
            self.assertEqual(moves[0].lines[3].credit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[3].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[3].amount_second_currency, Decimal('-10.0'))
            self.assertEqual(moves[0].lines[3].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[3].party, None)
            self.assertEqual(moves[0].lines[3].description, None)
            self.assertEqual(moves[0].lines[3].origin, None)
            self.assertEqual(len(moves[0].lines[3].tax_lines), 0)

            self.assertEqual(moves[0].lines[4].rec_name, 'Main Payable')
            self.assertEqual(moves[0].lines[4].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[4].debit, Decimal('9.52'))
            self.assertEqual(moves[0].lines[4].amount_second_currency, Decimal('10.0'))
            self.assertEqual(moves[0].lines[4].second_currency.rec_name, 'usd')
            self.assertEqual(moves[0].lines[4].party.rec_name, 'Party')
            self.assertEqual(moves[0].lines[4].description, None)
            self.assertEqual(moves[0].lines[4].origin.rec_name,
                '05/05/2022|Exp/Sp|-10.00 usd|buy something [-]')
            self.assertEqual(len(moves[0].lines[4].tax_lines), 0)

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

            rec_lines = Reconciliation.search([])
            rec_move_ids = [x.id for x in book.lines[0].moves[0].lines if x.party]
            self.assertEqual(len(rec_move_ids), 2)

            self.assertEqual(len(rec_lines), 1)
            self.assertEqual(len(rec_lines[0].lines), 2)

            self.assertTrue(rec_lines[0].lines[0].id in rec_move_ids)
            self.assertTrue(rec_lines[0].lines[1].id in rec_move_ids)

    @with_transaction()
    def test_line_check_wf_in_transfer(self):
        """ create cashbook + line, transfer: bank -> cash
            same currrency in both accounts
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Account = pool.get('account.account')
        AccountType = pool.get('account.account.type')
        Journal = pool.get('account.journal')
        Move = pool.get('account.move')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

            accounts = Account.create([{
                'name': 'Bankaccount',
                'code': '0123',
                'type': acc_type.id,
                }, {
                'name': 'Cashaccount',
                'code': '2345',
                'type': acc_type.id,
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Bankaccount')
            self.assertEqual(accounts[0].type.currency.code, 'usd')
            self.assertEqual(accounts[1].rec_name, '2345 - Cashaccount')
            self.assertEqual(accounts[1].type.currency.code, 'usd')
            self.assertEqual(company.currency.code, 'usd')

            books = Book.create([{
                'name': 'Book Bank',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }, {
                'name': 'Book Cash',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[1].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }])
            self.assertEqual(len(books), 2)
            self.assertEqual(books[0].rec_name, 'Book Bank | 0.00 usd | Open')
            self.assertEqual(books[0].account.rec_name, '0123 - Bankaccount')
            self.assertEqual(books[1].rec_name, 'Book Cash | 0.00 usd | Open')
            self.assertEqual(books[1].account.rec_name, '2345 - Cashaccount')

            # bank --> cash
            Book.write(*[
                [books[0]],
                {
                    'lines':[('create', [{
                        'bookingtype': 'mvout',
                        'amount': Decimal('10.0'),
                        'date': date(2022, 5, 5),
                        'description': 'from bank to cash',
                        'booktransf': books[1].id,
                        }])],
                }])

            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|to|-10.00 usd|from bank to cash [Book Cash | 0.00 usd | Open]')
            self.assertEqual(len(books[0].lines[0].moves), 0)
            self.assertEqual(books[0].lines[0].category, None)
            self.assertEqual(books[0].lines[0].party, None)

            self.assertEqual(len(books[1].lines), 0)
            self.assertEqual(Move.search_count([]), 0)

            Line.wfcheck([books[0].lines[0]])

            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|to|-10.00 usd|from bank to cash [Book Cash | 10.00 usd | Open]')
            self.assertEqual(books[1].lines[0].rec_name,
                '05/05/2022|from|10.00 usd|from bank to cash [Book Bank | -10.00 usd | Open]')
            self.assertEqual(len(books[1].lines[0].moves), 0)
            self.assertEqual(books[1].lines[0].category, None)
            self.assertEqual(books[1].lines[0].party, None)

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 2)
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(len(books[1].lines[0].moves), 0)

            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'from bank to cash')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|to|-10.00 usd|from bank to cash [Book Cash | 10.00 usd | Open]')
            self.assertEqual(moves[0].lines[0].rec_name, '(0123 - Bankaccount)')
            self.assertEqual(moves[0].lines[0].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].rec_name, '2345 - Cashaccount')
            self.assertEqual(moves[0].lines[1].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)

            # delete move
            Line.wfedit([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 0)

            # create move again
            Line.wfcheck([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'draft')

            # post move
            Line.wfdone([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'posted')

    @with_transaction()
    def test_line_check_wf_out_transfer(self):
        """ create cashbook + line, transfer: cash -> bank
            same currrency in both accounts
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Account = pool.get('account.account')
        AccountType = pool.get('account.account.type')
        Journal = pool.get('account.journal')
        Move = pool.get('account.move')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

            accounts = Account.create([{
                'name': 'Bankaccount',
                'code': '0123',
                'type': acc_type.id,
                }, {
                'name': 'Cashaccount',
                'code': '2345',
                'type': acc_type.id,
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Bankaccount')
            self.assertEqual(accounts[0].type.currency.code, 'usd')
            self.assertEqual(accounts[1].rec_name, '2345 - Cashaccount')
            self.assertEqual(accounts[1].type.currency.code, 'usd')
            self.assertEqual(company.currency.code, 'usd')

            books = Book.create([{
                'name': 'Book Bank',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }, {
                'name': 'Book Cash',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[1].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }])
            self.assertEqual(len(books), 2)
            self.assertEqual(books[0].rec_name, 'Book Bank | 0.00 usd | Open')
            self.assertEqual(books[0].account.rec_name, '0123 - Bankaccount')
            self.assertEqual(books[1].rec_name, 'Book Cash | 0.00 usd | Open')
            self.assertEqual(books[1].account.rec_name, '2345 - Cashaccount')

            # cash --> bank
            Book.write(*[
                [books[0]],
                {
                    'lines':[('create', [{
                        'bookingtype': 'mvin',
                        'amount': Decimal('10.0'),
                        'date': date(2022, 5, 5),
                        'description': 'from cash to bank',
                        'booktransf': books[1].id,
                        }])],
                }])

            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|from|10.00 usd|from cash to bank [Book Cash | 0.00 usd | Open]')
            self.assertEqual(len(books[0].lines[0].moves), 0)
            self.assertEqual(books[0].lines[0].category, None)
            self.assertEqual(books[0].lines[0].party, None)

            self.assertEqual(len(books[1].lines), 0)
            self.assertEqual(Move.search_count([]), 0)

            Line.wfcheck([books[0].lines[0]])

            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|from|10.00 usd|from cash to bank [Book Cash | -10.00 usd | Open]')
            self.assertEqual(books[1].lines[0].rec_name,
                '05/05/2022|to|-10.00 usd|from cash to bank [Book Bank | 10.00 usd | Open]')
            self.assertEqual(len(books[1].lines[0].moves), 0)
            self.assertEqual(books[1].lines[0].category, None)
            self.assertEqual(books[1].lines[0].party, None)

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 2)
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(len(books[1].lines[0].moves), 0)

            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'from cash to bank')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|from|10.00 usd|from cash to bank [Book Cash | -10.00 usd | Open]')
            self.assertEqual(moves[0].lines[0].rec_name, '0123 - Bankaccount')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Cashaccount)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)

            # delete move
            Line.wfedit([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 0)

            # create move again
            Line.wfcheck([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'draft')

            # post move
            Line.wfdone([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'posted')

    @with_transaction()
    def test_line_check_wf_out_transfer_2nd_currency(self):
        """ create cashbook + line, transfer: EURO <-- USD,
            different currrencies
        """
        pool = Pool()
        Book = pool.get('cashbook.book')
        Line = pool.get('cashbook.line')
        Configuration = pool.get('cashbook.configuration')
        Account = pool.get('account.account')
        AccountType = pool.get('account.account.type')
        Journal = pool.get('account.journal')
        Move = pool.get('account.move')

        types = self.prep_type()
        category = self.prep_category(cattype='in')
        company = self.prep_company()
        party = self.prep_party()
        cfg1 = self.prep_config()
        cfg1.cataccno = True
        cfg1.save()

        self.prep_accounting(company)
        # add EURO, set company-currency to EURO
        (usd, euro) = self.prep_2nd_currency(company)

        with Transaction().set_context({
            'company': company.id,
            }):
            acc_type, = AccountType.search([('name', '=', 'Cash')])

            accounts = Account.create([{
                'name': 'Bankaccount',
                'code': '0123',
                'type': acc_type.id,
                }, {
                'name': 'Cashaccount',
                'code': '2345',
                'type': acc_type.id,
                }])
            self.assertEqual(accounts[0].rec_name, '0123 - Bankaccount')
            self.assertEqual(accounts[0].type.currency.code, 'EUR')
            self.assertEqual(accounts[1].rec_name, '2345 - Cashaccount')
            self.assertEqual(accounts[1].type.currency.code, 'EUR')
            self.assertEqual(company.currency.code, 'EUR')

            books = Book.create([{
                'name': 'Book EURO',
                'btype': types.id,
                'company': company.id,
                'currency': company.currency.id,    # EURO
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[0].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }, {
                'name': 'Book USD',
                'btype': types.id,
                'company': company.id,
                'currency': usd.id,
                'number_sequ': self.prep_sequence().id,
                'start_date': date(2022, 5, 1),
                'account': accounts[1].id,
                'journal': Journal.search([('name', '=', 'Cashbook')])[0].id,
                'party_account': False,
                }])
            self.assertEqual(len(books), 2)
            self.assertEqual(books[0].rec_name, 'Book EURO | 0.00 € | Open')
            self.assertEqual(books[0].account.rec_name, '0123 - Bankaccount')
            self.assertEqual(books[1].rec_name, 'Book USD | 0.00 usd | Open')
            self.assertEqual(books[1].account.rec_name, '2345 - Cashaccount')

            # Euro <-- USD
            Book.write(*[
                [books[0]],
                {
                    'lines':[('create', [{
                        'bookingtype': 'mvin',
                        'amount': Decimal('10.0'),
                        'date': date(2022, 5, 5),
                        'description': 'EURO <-- USD',
                        'booktransf': books[1].id,
                        }])],
                }])

            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|from|10.00 €|EURO <-- USD [Book USD | 0.00 usd | Open]')
            self.assertEqual(len(books[0].lines[0].moves), 0)
            self.assertEqual(books[0].lines[0].category, None)
            self.assertEqual(books[0].lines[0].party, None)

            self.assertEqual(len(books[1].lines), 0)
            self.assertEqual(Move.search_count([]), 0)

            Line.wfcheck([books[0].lines[0]])

            self.assertEqual(len(books[0].lines), 1)
            self.assertEqual(books[0].lines[0].rec_name,
                '05/05/2022|from|10.00 €|EURO <-- USD [Book USD | -10.50 usd | Open]')
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].category, None)
            self.assertEqual(books[0].lines[0].party, None)

            self.assertEqual(len(books[1].lines), 1)
            self.assertEqual(books[1].lines[0].rec_name,
                '05/05/2022|to|-10.50 usd|EURO <-- USD [Book EURO | 10.00 € | Open]')
            self.assertEqual(len(books[1].lines[0].moves), 0)
            self.assertEqual(books[1].lines[0].category, None)
            self.assertEqual(books[1].lines[0].party, None)

            moves = Move.search([])
            self.assertEqual(len(moves), 1)
            self.assertEqual(len(moves[0].lines), 2)

            self.assertEqual(moves[0].state, 'draft')
            self.assertEqual(moves[0].date, date(2022, 5, 5))
            self.assertEqual(moves[0].description, 'EURO <-- USD')
            self.assertEqual(moves[0].period.rec_name, '2022-05')
            self.assertEqual(moves[0].journal.rec_name, 'Cashbook')
            self.assertEqual(moves[0].origin.rec_name,
                '05/05/2022|from|10.00 €|EURO <-- USD [Book USD | -10.50 usd | Open]')
            self.assertEqual(moves[0].lines[0].rec_name, '0123 - Bankaccount')
            self.assertEqual(moves[0].lines[0].credit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[0].debit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[0].amount_second_currency, None)
            self.assertEqual(moves[0].lines[1].rec_name, '(2345 - Cashaccount)')
            self.assertEqual(moves[0].lines[1].credit, Decimal('10.0'))
            self.assertEqual(moves[0].lines[1].debit, Decimal('0.0'))
            self.assertEqual(moves[0].lines[1].amount_second_currency, None)

            # delete move
            Line.wfedit([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 0)

            # create move again
            Line.wfcheck([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'draft')

            # post move
            Line.wfdone([books[0].lines[0]])
            self.assertEqual(len(books[0].lines[0].moves), 1)
            self.assertEqual(books[0].lines[0].moves[0].state, 'posted')

# end LineTestCase

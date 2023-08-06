# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.exceptions import UserError
from trytond.modules.cashbook.tests import CashbookTestCase
from trytond.modules.account.tests import create_chart, get_fiscalyear
from trytond.modules.company.tests import set_company
from datetime import date
from decimal import Decimal


class CategoryTestCase(CashbookTestCase):
    'Test cashbook categoy module'
    module = 'cashbook_account'

    def prep_config(self):
        """ disable account-name-view
        """
        Configuration = Pool().get('cashbook.configuration')

        cfg1 = super(CategoryTestCase, self).prep_config()
        cfg1.cataccno = False
        cfg1.save()
        return cfg1

    def prep_accounting(self, company1):
        """ create account-plan, fiscalyear, etc.
        """
        pool = Pool()
        FiscalYear = pool.get('account.fiscalyear')
        Sequence = pool.get('ir.sequence')
        AccountJournal = pool.get('account.journal')

        with set_company(company1):
            with Transaction().set_context({
                'company': company1.id,
                }):
                chart1 = create_chart(company = company1, tax = True)

                fisc_year = get_fiscalyear(company1, today=date(2022, 5, 1))
                fisc_year.save()
                FiscalYear.create_period([fisc_year])

                journal_sequence, = Sequence.search([
                        ('sequence_type.name', '=', "Account Journal"),
                        ], limit=1)
                journal_book, = AccountJournal.create([{
                        'name': 'Cashbook',
                        'code': 'B1',
                        'type': 'general',
                        'sequence': journal_sequence.id,
                    }])

    @with_transaction()
    def test_category_create_with_account(self):
        """ create category + account
        """
        pool = Pool()
        Account = pool.get('account.account')
        Category = pool.get('cashbook.category')

        company = self.prep_company()

        with Transaction().set_context({
            'company': company.id,
            }):
            account, = Account.create([{
                'name': 'Account No 1',
                'code': '0123',
                }])

            cat1, = Category.create([{
                'name': 'Test 1',
                'description': 'Info',
                'account': account.id,
                }])
            self.assertEqual(cat1.name, 'Test 1')
            self.assertEqual(cat1.rec_name, 'Test 1 [0123]')
            self.assertEqual(cat1.description, 'Info')
            self.assertEqual(cat1.company.rec_name, 'm-ds')

            self.assertEqual(Category.search_count([
                    ('account_code', '=', '0123'),
                ]), 1)
            self.assertEqual(Category.search_count([
                    ('account_code', '=', '123'),
                ]), 0)

# end CategoryTestCase

# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from decimal import Decimal
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.report import Report
from trytond.exceptions import UserError
from trytond.modules.cashbook.line import STATES, DEPENDS, sel_linetype, sel_bookingtype
from trytond.modules.cashbook.book import sel_state_book


class TaxLine(ModelSQL, ModelView):
    'Tax Line'
    __name__ = 'cashbook_account.tax'

    line = fields.Many2One(string='Line', model_name='cashbook.line',
        readonly=True, select=True, required=True, ondelete='CASCADE')
    splitline = fields.Many2One(string='Split Booking', model_name='cashbook.split',
        readonly=True, select=True, ondelete='CASCADE')

    tax = fields.Many2One(string='Tax', model_name='account.tax',
        states=STATES, depends=DEPENDS, required=True)
    base = fields.Numeric(string='Base', required=True,
        digits=(16, Eval('currency_digits', 2)),
        states=STATES, depends=DEPENDS+['currency_digits'])
    amount = fields.Numeric(string='Amount', required=True,
        digits=(16, Eval('currency_digits', 2)),
        states=STATES, depends=DEPENDS+['currency_digits'])

    currency = fields.Function(fields.Many2One(model_name='currency.currency',
        string="Currency", readonly=True), 'on_change_with_currency')
    currency_digits = fields.Function(fields.Integer(string='Currency Digits',
        readonly=True), 'on_change_with_currency_digits')
    bookingtype = fields.Function(fields.Selection(string='Type', readonly=True,
        selection=sel_bookingtype), 'on_change_with_bookingtype')
    state = fields.Function(fields.Selection(string='State', readonly=True,
        selection=sel_linetype), 'on_change_with_state')
    state_cashbook = fields.Function(fields.Selection(string='State of Cashbook',
        readonly=True, states={'invisible': True}, selection=sel_state_book),
        'on_change_with_state_cashbook')

    @classmethod
    def __setup__(cls):
        super(TaxLine, cls).__setup__()
        cls._order.insert(0, ('tax.name', 'ASC'))

    def get_rec_name(self, name):
        """ short + name
        """
        return '%(taxname)s %(amount)s %(base)s' % {
            'taxname': getattr(self.tax, 'rec_name'),
            'amount': Report.format_currency(self.amount or Decimal('0.0'),
                None, self.currency),
            'base': Report.format_currency(self.base or Decimal('0.0'),
                None, self.currency),
            }

    @fields.depends('line', '_parent_line.state')
    def on_change_with_state(self, name=None):
        """ get state
        """
        if self.line:
            return self.line.state

    @fields.depends('line', '_parent_line.cashbook')
    def on_change_with_state_cashbook(self, name=None):
        """ get state of cashbook
        """
        if self.line:
            return self.line.cashbook.state

    @fields.depends('line', '_parent_line.bookingtype')
    def on_change_with_bookingtype(self, name=None):
        """ get type
        """
        if self.line:
            return self.line.bookingtype

    @fields.depends('line', '_parent_line.cashbook')
    def on_change_with_currency(self, name=None):
        """ currency of cashbook
        """
        if self.line:
            return self.line.cashbook.currency.id

    @fields.depends('line', '_parent_line.cashbook')
    def on_change_with_currency_digits(self, name=None):
        """ currency-digits of cashbook
        """
        if self.line:
            return self.line.cashbook.currency.digits
        else:
            return 2

# end TaxLine

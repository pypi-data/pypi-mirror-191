# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.


from trytond.model import fields
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.pyson import Eval, And, Or, Bool
from trytond.pool import Pool
from trytond.modules.cashbook.line import STATES, DEPENDS
from decimal import Decimal


dep_taxena = ['ena_tax0', 'amount_tax0','ena_tax1', 'amount_tax1',
    'ena_tax2', 'amount_tax2', 'amount_net', 'amount', 'category']


class NetMixin:
    amount_net = fields.Function(fields.Numeric(string='Net',
        help='Net Amount of current booking.', readonly=True,
        digits=(16, Eval('currency_digits', 2)),
        states={
            'invisible': ~Bool(Eval('category')),
        }, depends=['currency_digits', 'category']),
        'on_change_with_amount_net')

    ena_tax0 = fields.Boolean(string='Tax Null',
        states={
            'readonly': Or(
                STATES['readonly'],
                Eval('avail_tax0', False) == False,
                ),
        }, depends=DEPENDS+['avail_tax0'])
    amount_tax0 = fields.Function(fields.Numeric(string='Tax Null',
        digits=(16, Eval('currency_digits', 2)), readonly=True,
        depends=['currency_digits']),
        'on_change_with_amount_tax0')

    ena_tax1 = fields.Boolean(string='Tax Half',
        states={
            'readonly': Or(
                STATES['readonly'],
                Eval('avail_tax1', False) == False,
                ),
        }, depends=DEPENDS+['avail_tax1'])
    amount_tax1 = fields.Function(fields.Numeric(string='Tax Half',
        digits=(16, Eval('currency_digits', 2)), readonly=True,
        depends=['currency_digits']),
        'on_change_with_amount_tax1')

    ena_tax2 = fields.Boolean(string='Tax Full',
        states={
            'readonly': Or(
                STATES['readonly'],
                Eval('avail_tax2', False) == False,
                ),
        }, depends=DEPENDS+['avail_tax2'])
    amount_tax2 = fields.Function(fields.Numeric(string='Tax Full',
        digits=(16, Eval('currency_digits', 2)), readonly=True,
        depends=['currency_digits']),
        'on_change_with_amount_tax2')

    avail_tax0 = fields.Function(fields.Boolean(string='Tax Null available',
        states={'invisible': True}, readonly=True), 'on_change_with_avail_tax0')
    avail_tax1 = fields.Function(fields.Boolean(string='Tax Half available',
        states={'invisible': True}, readonly=True), 'on_change_with_avail_tax1')
    avail_tax2 = fields.Function(fields.Boolean(string='Tax Full available',
        states={'invisible': True}, readonly=True), 'on_change_with_avail_tax2')

    @classmethod
    def default_ena_tax0(cls):
        """ default: False
        """
        return False

    @classmethod
    def default_ena_tax1(cls):
        """ default: False
        """
        return False

    @classmethod
    def default_ena_tax2(cls):
        """ default: False
        """
        return False

    def get_list_of_taxes(self):
        """ get taxes for current line or split-line,
            in cashbook-currency
        """
        pool = Pool()
        Tax = pool.get('account.tax')
        IrDate = pool.get('ir.date')

        if self.category is None:
            return []

        # get enabled tax-fields
        taxes = []
        for x in range(3):
            if getattr(self.category, 'tax%d' % x, None) is None:
                continue

            if getattr(self, 'ena_tax%d' % x) == True:
                taxes.append(getattr(self.category, 'tax%d' % x))

        if len(taxes) == 0:
            return []

        if self.date is None:
            date_line = IrDate.today()
        else :
            date_line = self.date

        # get net from gross and taxes
        net_amount = self.currency.round(
                Tax.reverse_compute(self.amount, taxes, date_line))

        # get taxes from net
        tax_lines = Tax.compute(taxes, net_amount, Decimal('1.0'), date_line)
        total = self.amount # gross
        tax_lines2 = []
        for tax_line in tax_lines:
            tax_lines2.append({
                'amount': self.currency.round(tax_line['amount']),
                'tax': tax_line['tax'],
                })
            # gross - tax = net
            total -= self.currency.round(tax_line['amount'])

        for pos in range(len(tax_lines2)):
            tax_lines2[pos]['base'] = total
        return tax_lines2

    @fields.depends('taxes')
    def on_change_with_amount_net(self, name=None):
        """ compute net from tax-lines
        """
        # one or more lines - we use 'base'
        for tax_line in self.taxes:
            if (self.__name__ == 'cashbook.line') and \
                (tax_line.splitline is not None):
                # tax-lines for split-bookings are store here
                # skip them
                continue
            return tax_line.base
        return None

    def mxin_compute_tax_amount(self, tax_no):
        """ compute tax for selected line
        """
        pool = Pool()
        TaxLine = pool.get('cashbook_account.tax')
        Tax = pool.get('account.tax')

        tax_amount = None
        if self.category:
            tax_select = getattr(self.category, 'tax%d' % tax_no, None)
            if tax_select:
                for tax_line in self.taxes:

                    if (self.__name__ == 'cashbook.line') and \
                        (tax_line.splitline is not None):
                        continue

                    if tax_line.tax is None:
                        continue

                    # check if current line relates to selected tax
                    if Tax.search_count([
                        ('parent', 'child_of', tax_select.id),
                        ('id', '=', tax_line.tax.id),
                        ]) > 0:
                        if tax_amount is None:
                            tax_amount = Decimal('0.0')
                        tax_amount += tax_line.amount
        return tax_amount

    @fields.depends('taxes', 'category', '_parent_category.tax0')
    def on_change_with_amount_tax0(self, name=None):
        """ compute tax0 from tax-lines
        """
        return self.mxin_compute_tax_amount(0)

    @fields.depends('taxes', 'category', '_parent_category.tax1')
    def on_change_with_amount_tax1(self, name=None):
        """ compute tax0 from tax-lines
        """
        return self.mxin_compute_tax_amount(1)

    @fields.depends('taxes', 'category', '_parent_category.tax2')
    def on_change_with_amount_tax2(self, name=None):
        """ compute tax2 from tax-lines
        """
        return self.mxin_compute_tax_amount(2)

    @fields.depends('category', '_parent_category.tax0')
    def on_change_with_avail_tax0(self, name=None):
        """ get True if tax is used on category,
            depends on configured taxes on category
        """
        if self.category:
            if self.category.tax0:
                return True
        return False

    @fields.depends('category', '_parent_category.tax1')
    def on_change_with_avail_tax1(self, name=None):
        """ get True if tax is used on category,
            depends on configured taxes on category
        """
        if self.category:
            if self.category.tax1:
                return True
        return False

    @fields.depends('category', '_parent_category.tax2')
    def on_change_with_avail_tax2(self, name=None):
        """ get True if tax is used on category,
            depends on configured taxes on category
        """
        if self.category:
            if self.category.tax2:
                return True
        return False

    @classmethod
    def validate(cls, lines):
        """ check amounts and taxes
        """
        super(NetMixin, cls).validate(lines)
        cls.check_tax_amounts(lines)

    @classmethod
    def check_tax_amounts(cls, lines):
        """ check amounts and taxes
        """
        for line in lines:
            if line.__name__ == 'cashbook.line':
                if not line.bookingtype in ['in', 'out']:
                    for x in range(3):
                        if getattr(line, 'ena_tax%d' % x) != False:
                            raise UserError(gettext(
                                'cashbook_account.msg_line_tax_must_disabled',
                                linename = line.rec_name,
                                ))

    @classmethod
    def get_taxlines_updates(cls, records):
        """ get to_create, to_delete
        """
        to_del = []
        to_create = []
        for record in records:
            if record.__name__ == 'cashbook.line':
                to_del.extend([x for x in record.taxes if x.splitline is None])
            elif record.__name__ == 'cashbook.split':
                to_del.extend([x for x in record.taxes if getattr(x.splitline, 'id', None) == record.id])

            lines = []
            for tax in record.get_list_of_taxes():
                r1 = {
                    'line': record.id if record.__name__ == 'cashbook.line' else record.line.id,
                    'splitline': None if record.__name__ == 'cashbook.line' else record.id,
                    }
                r1.update(tax)
                r1['tax'] = r1['tax'].id
                lines.append(r1)
            if len(lines) > 0:
                to_create.extend(lines)
        return (to_create, to_del)

    @classmethod
    def create(cls, vlist):
        """ add tax-lines
        """
        TaxLine = Pool().get('cashbook_account.tax')

        records = super(NetMixin, cls).create(vlist)
        (to_create, to_del) = cls.get_taxlines_updates(records)

        if len(to_del) > 0:
            TaxLine.delete(to_del)
        if len(to_create) > 0:
            TaxLine.create(to_create)

        return records

    @classmethod
    def write(cls, *args):
        """ add/update tax-lines
        """
        TaxLine = Pool().get('cashbook_account.tax')

        to_update_record = []
        actions = iter(args)
        for records, values in zip(actions, actions):
            if len(set({'amount', 'category', 'ena_tax0', 'ena_tax1',
                'ena_tax2'}).intersection(values.keys())) > 0:
                to_update_record.extend(records)

        super(NetMixin, cls).write(*args)

        (to_create, to_del) = cls.get_taxlines_updates(to_update_record)

        if len(to_del) > 0:
            TaxLine.delete(to_del)
        if len(to_create) > 0:
            TaxLine.create(to_create)

# end NetMixin

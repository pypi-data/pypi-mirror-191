# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, And, Bool, Or
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.transaction import Transaction
from decimal import Decimal
from trytond.modules.cashbook.line import STATES, DEPENDS
from .netmixin import NetMixin


dep_taxena = ['ena_tax0', 'ena_tax1', 'ena_tax2', 'amount', 'taxes', 'category',
    'date', 'currency', '_parent_category.tax0', '_parent_category.tax1',
    '_parent_category.tax2']
dep_taxes = dep_taxena + ['amount_tax0', 'amount_tax1', 'amount_tax2', 'amount_net']
dep_bookingtype = dep_taxena+['bookingtype', 'category', 'splitlines']


class Line(NetMixin, metaclass=PoolMeta):
    __name__ = 'cashbook.line'

    taxes = fields.One2Many(string='Tax Lines', field='line',
        model_name='cashbook_account.tax', readonly=True,
        states={
            'invisible': ~Or(
                    And(
                        Eval('bookingtype', '').in_(['in', 'out']),
                        Bool(Eval('category')),
                    ),
                    Eval('bookingtype', '').in_(['spin', 'spout']),
                ),
        }, depends=['category', 'bookingtype'])
    moves = fields.One2Many(string='Moves', model_name='account.move',
        field='origin', readonly=True, size=1,
        states={
            'invisible': ~Bool(Eval('moves')),
        })
    account_cashbook = fields.Function(fields.Many2One(readonly=True,
        string='Account Cashbook', model_name='account.account',
        states={'invisible': True}),
        'on_change_with_account_cashbook')
    party_required = fields.Function(fields.Boolean(string='Party required',
        readonly=True, states={'invisible': True}),
        'on_change_with_party_required')

    @classmethod
    def __setup__(cls):
        super(Line, cls).__setup__()
        requ_cond = And(
                Eval('bookingtype', '').in_(['in', 'out']),
                Eval('party_required', False) == True,
            )
        if cls.party.states.get('required', None) is None:
            cls.party.states['required'] = requ_cond
        else :
            cls.party.states['required'] = Or(cls.party.states['required'], requ_cond)
        cls.party.depends.append('party_required')

    @classmethod
    def wfedit(cls, lines):
        """ delete moves
        """
        Move = Pool().get('account.move')

        to_delete_move = []
        for line in lines:
            to_delete_move.extend([
                    move for move in line.moves if move.state == 'draft'
                ])

        super(Line, cls).wfedit(lines)
        if len(to_delete_move) > 0:
            Move.delete(to_delete_move)

    @classmethod
    def wfcheck(cls, lines):
        """ add moves
        """
        pool = Pool()
        Move = pool.get('account.move')
        Period = pool.get('account.period')

        super(Line, cls).wfcheck(lines)

        to_create_move = []
        for line in lines:
            if len(line.moves) > 0:
                continue
            if line.reference:
                continue

            if line.cashbook.account:
                move_data = {
                    'date': line.date,
                    'description': line.description,
                    'period': Period.find(line.cashbook.company.id, line.date),
                    'journal': line.cashbook.journal.id,
                    'origin': (line.__name__, line.id),
                    'lines': [],
                    }
                move_lines = []

                if (line.bookingtype in ['out', 'in']):
                    move_lines.extend(cls.get_move_lines_by_category(line))
                elif (line.bookingtype in ['spout', 'spin']):
                    move_lines.extend(cls.get_move_lines_by_splitbooking(line))
                elif (line.bookingtype in ['mvout', 'mvin']):
                    move_lines.extend(cls.get_move_lines_by_transfer(line))
                else :
                    raise ValueError('invalid bookingtype')

                move_data['lines'].append(('create', move_lines))
                to_create_move.append(move_data)

        if len(to_create_move) > 0:
            Move.create(to_create_move)

    @classmethod
    def wfdone(cls, lines):
        """ post moves
        """
        pool = Pool()
        Move = pool.get('account.move')
        Line2 = pool.get('account.move.line')

        super(Line, cls).wfdone(lines)

        to_post = []
        to_reconcile = []
        for line in lines:
            for move in line.moves:
                if move.state == 'draft':
                    to_post.append(move)

                recon_lines = [move_line for move_line in move.lines if move_line.party]
                if len(recon_lines) > 0:
                    to_reconcile.append(recon_lines)
        Move.post(to_post)
        Line2.reconcile(*to_reconcile)

    @fields.depends(*dep_taxes)
    def on_change_taxes(self):
        """ update amounts
        """
        self.amount_net = self.on_change_with_amount_net()
        self.amount_tax0 = self.on_change_with_amount_tax0()
        self.amount_tax1 = self.on_change_with_amount_tax1()
        self.amount_tax2 = self.on_change_with_amount_tax2()

    def update_taxes(self):
        """ update tax_line-records
        """
        TaxLine = Pool().get('cashbook_account.tax')

        taxes = self.get_list_of_taxes()
        tax_dict = {x['tax'].id:x for x in taxes}

        to_delete = []
        for tax_line in self.taxes:
            if tax_line.splitline is not None:
                continue

            if tax_line.tax.id not in tax_dict.keys():
                to_delete.append(tax_line)

            if tax_line.tax.id in tax_dict.keys():
                tax_line.base = tax_dict[tax_line.tax.id]['base']
                tax_line.amount = tax_dict[tax_line.tax.id]['amount']
                del tax_dict[tax_line.tax.id]

        l1 = []
        # delete
        for tax in list(self.taxes):
            if tax in to_delete:
                continue
            l1.append(tax)

        # add missing taxes
        for tax in tax_dict.keys():
            l1.append(TaxLine(
                amount = tax_dict[tax]['amount'],
                base =  tax_dict[tax]['base'],
                tax =  tax_dict[tax]['tax'],
                splitline = None,
                ))
        self.taxes = l1

    @fields.depends(*dep_bookingtype)
    def on_change_bookingtype(self):
        """ update category
        """
        super(Line, self).on_change_bookingtype()
        self.on_change_category()

    @fields.depends(*dep_taxena)
    def on_change_category(self):
        """ update net+taxes
        """
        for x in range(3):
            setattr(self, 'ena_tax%d' % x, False)
        self.update_taxes()
        self.on_change_taxes()

    @fields.depends(*dep_taxena)
    def on_change_amount(self):
        """ update net+taxes
        """
        super(Line, self).on_change_amount()
        self.update_taxes()
        self.on_change_taxes()

    @fields.depends(*dep_taxena)
    def on_change_ena_tax0(self):
        """ clear amount on disable
        """
        self.update_taxes()
        self.on_change_taxes()

    @fields.depends(*dep_taxena)
    def on_change_ena_tax1(self):
        """ clear amount on disable
        """
        self.update_taxes()
        self.on_change_taxes()

    @fields.depends(*dep_taxena)
    def on_change_ena_tax2(self):
        """ clear amount on disable
        """
        self.update_taxes()
        self.on_change_taxes()

    @classmethod
    def get_inverted_move_values(cls, values):
        """ credit -> debit, debit, -> credit etc.
        """
        if values['amount_second_currency'] is None:
            amount = None
        else :
            amount = values['amount_second_currency'].copy_negate()

        return {
            'credit': values['debit'],
            'debit': values['credit'],
            'second_currency': values['second_currency'],
            'amount_second_currency': amount,
            }

    @classmethod
    def get_move_amounts(cls, line, amount):
        """ get credit/debit/2ndcurrency
        """
        Currency = Pool().get('currency.currency')

        amounts = {
            'amount_second_currency': None,
            'second_currency': None,
            }
        amounts.update(cls.get_debit_credit({
            'amount': amount,
            'bookingtype': line.bookingtype,
            }))

        if line.cashbook.currency.id != line.cashbook.company.currency.id:
            amounts['amount_second_currency'] = amount.copy_sign(
                    amounts['debit'] - amounts['credit']
                )
            amounts['second_currency'] = line.cashbook.currency.id

        with Transaction().set_context({
            'date': line.date,
            }):
            for x in ['credit', 'debit']:
                if line.cashbook.currency.id != line.cashbook.company.currency.id:
                    amounts[x] = Currency.compute(
                        line.cashbook.currency,
                        amounts[x],
                        line.cashbook.company.currency)
        return amounts

    @classmethod
    def get_article_lines(cls, line, description=None):
        """ get move-line of article
        """
        def get_taxline_amount(moveline):
            return moveline['debit'] - moveline['credit'] \
                if line.bookingtype.endswith('out') \
                        else moveline['credit'] - moveline['debit']

        move_lines = []

        # total-amount converted to company-currency
        total_amount = cls.get_move_amounts(line, line.amount)

        # line: category-account
        # convert to company currency
        move_line = {
            'account': line.category.account.id,
            'description': description,
            'origin': (line.__name__, line.id) \
                if line.__name__ == 'cashbook.split' else None,
            }
        move_line.update(cls.get_move_amounts(
            line,
            line.amount if line.amount_net is None else line.amount_net,
            ))

        if len(line.taxes) > 0:
            move_line['tax_lines'] = [('create', [{
                'amount': get_taxline_amount(move_line),
                'type': 'base',
                'tax': x.tax.id,
                } for x in line.taxes])]
        move_lines.append(move_line)

        # taxes are stored in line.taxes
        # must be converted to company-currency
        for tax in line.taxes:
            if line.__name__ == 'cashbook.line':
                if tax.splitline is not None:
                    continue
            elif line.__name__ == 'cashbook.split':
                # skip tax-lines for other split-lines
                if getattr(tax.splitline, 'id', None) != line.id:
                    continue

            if tax.amount >= Decimal('0.0'):
                tax_account = tax.tax.invoice_account.id
            else :
                tax_account = tax.tax.credit_note_account.id

            move_line = {
                'account': tax_account,
                'description': description,
                'origin': (line.__name__, line.id) \
                    if line.__name__ == 'cashbook.split' else None,
                }
            move_line.update(cls.get_move_amounts(
                line,
                tax.amount,
                ))
            # tax line
            move_line['tax_lines'] = [('create', [{
                'amount': get_taxline_amount(move_line),
                'type': 'tax',
                'tax': tax.tax.id,
                }])]
            move_lines.append(move_line)

        # check rounding errors debit/credit/2ndcurrency
        # fix it in last line
        move_lines[-1]['debit'] -= sum(x['debit'] for x in move_lines) - \
            total_amount['debit']
        move_lines[-1]['credit'] -= sum(x['credit'] for x in move_lines) - \
            total_amount['credit']
        if len(move_lines) > 1:
            move_lines[-1]['tax_lines'][0][1][0]['amount'] = get_taxline_amount(move_lines[-1])

        if total_amount['amount_second_currency'] is not None:
            move_lines[-1]['amount_second_currency'] -= \
                sum(x['amount_second_currency'] for x in move_lines) - \
                total_amount['amount_second_currency']
        return move_lines

    @classmethod
    def get_cashbook_lines(cls, line, amounts, description=None):
        """ get move-line of cashbook-transfer
        """
        move_line = {
            'account': line.booktransf.account.id,
            'description': description,
            'origin': (line.__name__, line.id) \
                if line.__name__ == 'cashbook.split' else None,
            }
        move_line.update(amounts)
        return [move_line]

    @classmethod
    def get_move_lines_by_splitbooking(cls, line):
        """ create move lines for splitbooking
        """
        # select account of party if enabled
        if line.cashbook.party_account == True:
            if line.bookingtype == 'spout':
                party_account = line.party.account_payable_used.id
            elif line.bookingtype == 'spin':
                party_account = line.party.account_receivable_used.id
            else :
                raise ValueError('invalid bookingtype: %s' % line.bookingtype)
        else :
            party_account = None

        # amounts of split-lines can be in 2nd-currency,
        # compute to company-currency
        move_lines = []
        for spline in line.splitlines:
            if spline.splittype == 'cat':
                if spline.category.account is None:
                    raise UserError(gettext(
                        'cashbook_account.msg_line_missing_category_account',
                        catname = spline.category.rec_name,
                        ))
                move_lines.extend(cls.get_article_lines(spline, spline.description))
            elif spline.splittype == 'tr':
                if spline.booktransf.account is None:
                    raise UserError(gettext(
                        'cashbook_account.msg_line_missing_book_account',
                        bookname = spline.booktransf.rec_name,
                        ))
                amounts = cls.get_move_amounts(spline, spline.amount)
                move_lines.extend(cls.get_cashbook_lines(spline, amounts, spline.description))
            else :
                raise ValueError('invalid splittype: %s' % spline.splittype)

        # book-line
        book_line = {
            'account': line.cashbook.account.id,
            }
        amounts = cls.get_move_amounts(line, line.amount)
        amounts_invers = cls.get_inverted_move_values(amounts)
        book_line.update(amounts_invers)
        move_lines.append(book_line)

        if party_account:
            party_line = {
                'account':  party_account,
                'party': line.party.id,
                'origin': (line.__name__, line.id),
                }

            pline1 = {}
            pline1.update(party_line)
            pline1.update(amounts_invers)
            move_lines.insert(0, pline1)

            pline2 = {}
            pline2.update(party_line)
            pline2.update(amounts)
            move_lines.append(pline2)

        move_lines.reverse()
        return move_lines

    @classmethod
    def get_move_lines_by_category(cls, line):
        """ create move lines if a category and party was used
        """
        if line.category.account is None:
            raise UserError(gettext(
                'cashbook_account.msg_line_missing_category_account',
                catname = line.category.rec_name,
                ))

        # select account of party if enabled
        if line.cashbook.party_account == True:
            if (line.debit - line.credit) >= Decimal('0.0'):
                party_account = line.party.account_payable_used.id
            else :
                party_account = line.party.account_receivable_used.id
        else :
            party_account = None

        # gross-amounts of line with 2nd currency
        # convert to company-currency
        amounts = cls.get_move_amounts(line, line.amount)
        amounts_invers = cls.get_inverted_move_values(amounts)

        move_lines = []

        # party has/was payed
        if party_account:
            party_line = {
                'account':  party_account,
                'party': line.party.id,
                }
            party_line.update(amounts)
            move_lines.append(party_line)

        # book-account
        book_line = {
            'account': line.cashbook.account.id,
            }
        book_line.update(amounts_invers)
        move_lines.append(book_line)

        # category-account
        move_lines.extend(cls.get_article_lines(line))

        # party was charged
        if party_account:
            party_line = {
                'account':  party_account,
                'party': line.party.id,
                }
            party_line.update(amounts_invers)
            move_lines.append(party_line)

        return move_lines

    @classmethod
    def get_move_lines_by_transfer(cls, line):
        """ create move lines if amount was transferred
            between cashbooks
        """
        if line.booktransf.account is None:
            raise UserError(gettext(
                'cashbook_account.msg_line_missing_book_account',
                bookname = line.booktransf.rec_name,
                ))

        # target-book-account
        amounts = cls.get_move_amounts(line, line.amount)
        amounts_invers = cls.get_inverted_move_values(amounts)

        move_line = {'account': line.booktransf.account.id}
        move_line.update(amounts)

        # source-book-account
        move_line2 = {'account': line.cashbook.account.id}
        move_line2.update(amounts_invers)
        return [move_line, move_line2]

    @fields.depends('cashbook', '_parent_cashbook.party_account')
    def on_change_with_party_required(self, name=None):
        """ get state of checkbox
        """
        if self.cashbook:
            return self.cashbook.party_account

    @fields.depends('cashbook', '_parent_cashbook.account')
    def on_change_with_account_cashbook(self, name=None):
        """ get account
        """
        if self.cashbook:
            if self.cashbook.account:
                return self.cashbook.account.id

    @fields.depends('category')
    def on_change_with_category_view(self, name=None):
        """ show optimizef form of category for list-view
        """
        Configuration = Pool().get('cashbook.configuration')

        if self.category:
            cfg1 = Configuration.get_singleton()

            cat_name = super(Line, self).on_change_with_category_view(name)
            if getattr(cfg1, 'catnamelong', True) == True:
                return cat_name
            else :
                return self.category.get_long_recname(cat_name)

    @classmethod
    def search_category_view(cls, name, clause):
        """ search in category
        """
        return ['OR',
            super(Line, cls).search_category_view(name, clause),
            ('category.account.code',) + tuple(clause[1:]),
            ]

# end Line

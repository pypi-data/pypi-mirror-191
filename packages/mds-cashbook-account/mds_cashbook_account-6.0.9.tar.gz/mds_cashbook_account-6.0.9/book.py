# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool
from trytond.modules.cashbook.book import STATES2, DEPENDS2


class Book(metaclass=PoolMeta):
    __name__ = 'cashbook.book'

    account = fields.Many2One(string='Account', select=True,
        model_name='account.account', ondelete='RESTRICT',
        states=STATES2, depends=DEPENDS2+['company'],
        domain=[('company.id', '=', Eval('company', -1))])
    journal = fields.Many2One(string='Journal', ondelete='RESTRICT',
        model_name='account.journal',
        states={
            'readonly': STATES2['readonly'],
            'required': Bool(Eval('account')),
        }, depends=DEPENDS2+['account'])
    party_account = fields.Boolean(string='Involve party accounts',
        help='The Receivable/Payable accounts of the party are included in move line records.',
        states=STATES2, depends=DEPENDS2)

    @classmethod
    def default_party_account(cls):
        """ default: true
        """
        return True

# end Book

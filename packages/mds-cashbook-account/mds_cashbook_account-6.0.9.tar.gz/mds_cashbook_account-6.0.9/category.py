# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields, Unique
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool


STATES = {
    'readonly': ~Bool(Eval('account')),
    }
DEPENDS=['account']


class Category(metaclass=PoolMeta):
    __name__ = 'cashbook.category'

    account = fields.Many2One(string='Account', select=True,
        model_name='account.account', ondelete='RESTRICT')
    account_code = fields.Function(fields.Char(string='Account', readonly=True),
        'on_change_with_account_code', searcher='search_account_code')
    tax0 = fields.Many2One(string='Tax Null', model_name='account.tax',
        ondelete='RESTRICT', states=STATES, depends=DEPENDS)
    tax1 = fields.Many2One(string='Tax Half', model_name='account.tax',
        ondelete='RESTRICT', states=STATES, depends=DEPENDS)
    tax2 = fields.Many2One(string='Tax Full', model_name='account.tax',
        ondelete='RESTRICT', states=STATES, depends=DEPENDS)

    @classmethod
    def __setup__(cls):
        super(Category, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints.extend([
                ('account_uniq',
                    Unique(t, t.account, t.company),
                    'cashbook_account.msg_category_account_unique'),
            ])

    @fields.depends('account', 'tax0', 'tax1', 'tax2')
    def on_change_account(self):
        """ clear taxes if account is removed
        """
        if self.account is None:
            self.tax0 = None
            self.tax1 = None
            self.tax2 = None

    def get_long_recname(self, recname):
        """ build rec_name with account-no
        """
        Configuration = Pool().get('cashbook.configuration')

        l1 = [recname]

        if self.account:
            if self.account.code:
                cfg1 = Configuration.get_singleton()
                if getattr(cfg1, 'cataccno', True) == True:
                    l1.append('[%s]' % self.account.code)
        return ' '.join(l1)

    def get_rec_name(self, name):
        """ short + name
        """
        return self.get_long_recname(
                super(Category, self).get_rec_name(name)
            )

    @classmethod
    def search_rec_name(cls, name, clause):
        """ search in account + name
        """
        return ['OR',
            super(Category, cls).search_rec_name(name, clause),
            ('account.rec_name',) + tuple(clause[1:]),
            ('account.code',) + tuple(clause[1:]),
            ]

    @fields.depends('account')
    def on_change_with_account_code(self, name=None):
        """ get code of account
        """
        if self.account:
            return self.account.code

    @classmethod
    def search_account_code(cls, names, clause):
        """ search in code
        """
        return [('account.code',) + tuple(clause[1:])]

# end Category

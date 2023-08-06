# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import Pool, PoolMeta


field_cataccno = fields.Boolean(string='Category: Show account number',
    help='Shows the number of the linked account in the name of a category.')


class Configuration(metaclass=PoolMeta):
    __name__ = 'cashbook.configuration'

    cataccno = fields.MultiValue(field_cataccno)

    @classmethod
    def multivalue_model(cls, field):
        """ get model for value
        """
        pool = Pool()

        if field in ['cataccno']:
            return pool.get('cashbook.configuration_user')
        return super(Configuration, cls).multivalue_model(field)

    @classmethod
    def default_cataccno(cls, **pattern):
        return cls.multivalue_model('cataccno').default_cataccno()

# end Configuration


class UserConfiguration(metaclass=PoolMeta):
    __name__ = 'cashbook.configuration_user'

    cataccno = field_cataccno

    @classmethod
    def default_cataccno(cls):
        return True

# end UserConfiguration

# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import PoolMeta


class Move(metaclass=PoolMeta):
    __name__ = 'account.move'

    @classmethod
    def _get_origin(cls):
        """ add cashbook.line
        """
        l1 = ['cashbook.line']
        l1.extend(super(Move, cls)._get_origin())
        return l1

# end Move


class MoveLine(metaclass=PoolMeta):
    __name__ = 'account.move.line'

    @classmethod
    def _get_origin(cls):
        """ add cashbook.line+split
        """
        l1 = ['cashbook.line', 'cashbook.split']
        l1.extend(super(MoveLine, cls)._get_origin())
        return l1

# end MoveLine

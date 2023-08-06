# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from .netmixin import NetMixin


class SplitLine(NetMixin, metaclass=PoolMeta):
    __name__ = 'cashbook.split'

    taxes = fields.Function(fields.One2Many(string='Tax Lines', field=None,
        model_name='cashbook_account.tax', readonly=True),
        'on_change_with_taxes')

    @fields.depends('line', '_parent_line.taxes')
    def on_change_with_taxes(self, name=None):
        """ get taxes for current split-line
        """
        if self.line:
            return [x.id for x in self.line.taxes
                if getattr(x.splitline, 'id', None) == self.id]
        return []

# end SplitLine

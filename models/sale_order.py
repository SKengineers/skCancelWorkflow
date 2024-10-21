# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_cancel(self):
        inv = self.invoice_ids.filtered(lambda inv: inv.state != 'cancel')
        inv.button_cancel()
        for pick in self.picking_ids.filtered(lambda x: x.state == 'done'):
            pick.action_cancel_picking()
        for pick in self.picking_ids.filtered(lambda x: x.state not in ['done', 'cancel']):
            pick.action_cancel()
        account_payment = self.env['account.payment'].search([
            ('reconciled_invoice_ids', 'in', self.ids),
            ('state', '!=', 'cancel')
        ])
        for payment in account_payment:
            payment.action_cancel()
        return self.write({'state': 'cancel'})
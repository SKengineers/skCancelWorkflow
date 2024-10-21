# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_cancel_purchase(self):
        for pur in self:
            for pick in pur.picking_ids.filtered(lambda x: x.state == 'done'):
                pick.action_cancel_picking()
            for pick in pur.picking_ids.filtered(lambda x: x.state not in ['done', 'cancel']):
                pick.action_cancel()
            for inv in pur.invoice_ids.filtered(lambda x: x.state != 'cancel'):
                inv.button_cancel()
                account_payment = self.env['account.payment'].search([
                    ('reconciled_bill_ids', 'in', inv.ids),
                    ('state', '!=', 'cancel')
                ])
                for pay in account_payment:
                    pay.action_cancel()
            pur.state = 'cancel'

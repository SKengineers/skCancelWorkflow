# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError


class WizardCancelSetToDraft(models.TransientModel):
    _name = 'wizard.cancel.draft.work.flow'
    _description = "Cancel/Set To Draft Work Flow"

    name = fields.Char(string='Name')
    type = fields.Selection([
        ('cancel', 'Cancel'),
        ('set_to_draft', 'Set To Draft')
    ], string='Type', default=None)

    def action_cancel(self):
        active_model = self.env.context.get('active_model')
        if active_model == 'stock.picking':
            stock_picking_ids = self.env['stock.picking'].search([
                ('id', 'in', self.env.context.get('active_ids'))
            ])
            for stock in stock_picking_ids:
                if stock.state == 'done':
                    stock.action_cancel_picking()
                elif stock.state not in ['done', 'cancel']:
                    stock.action_cancel()
        if active_model == 'purchase.order':
            purchase_order_ids = self.env['purchase.order'].search([
                ('id', 'in', self.env.context.get('active_ids'))
            ])
            for purchase in purchase_order_ids:
                if purchase.state == 'purchase':
                    purchase.action_cancel_purchase()
                else:
                    purchase.button_cancel()
        if active_model == 'account.move':
            account_move_ids = self.env['account.move'].search([
                ('id', 'in', self.env.context.get('active_ids'))
            ])
            for move in account_move_ids:
                if move.move_type in ['out_invoice', 'in_invoice']:
                    move.button_cancel()

    def action_set_to_draft(self):
        return True

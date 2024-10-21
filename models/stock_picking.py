# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for rec in self:
            account_move = self.env['account.move'].search([
                ('move_type', '=', 'entry'),
                ('ref', 'like', rec.name),
                ('state', '!=', 'cancel')
            ])
            if account_move:
                account_move.write({
                    'picking_id': rec.id
                })
        return res

    def action_cancel_picking(self):
        for record in self:
            if record.state == 'done':
                if record.picking_type_id.code == 'outgoing':
                    for line in record.move_line_ids_without_package:
                        if line.lot_id:
                            self.env['stock.quant']._update_available_quantity(line.product_id, line.location_id, line.quantity, lot_id=line.lot_id)
                        else:
                            self.env['stock.quant']._update_available_quantity(line.product_id, line.location_id, line.quantity)
                if record.picking_type_id.code == 'incoming':
                    for line in record.move_line_ids_without_package:
                        if line.lot_id:
                            self.env['stock.quant']._update_available_quantity(line.product_id, line.location_dest_id, -1 * line.quantity, lot_id=line.lot_id)
                        else:
                            self.env['stock.quant']._update_available_quantity(line.product_id, line.location_dest_id, -1 * line.quantity)
                record.state = 'cancel'
                for move in record.move_ids_without_package:
                    move.state = 'cancel'
                for move_line in record.move_line_ids_without_package:
                    move_line.state = 'cancel'
                account_move_entry = self.env['account.move'].search([
                    ('picking_id', '=', record.id),
                    ('state', '!=', 'cancel')
                ])
                if account_move_entry:
                    account_move_entry.button_cancel()

    def action_set_to_draft_picking(self):
        for record in self:
            record.state = 'draft'
            for move in record.move_ids_without_package:
                move.state = 'draft'
            for move_line in record.move_line_ids_without_package:
                move_line.state = 'draft'

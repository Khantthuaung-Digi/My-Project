# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for record in self:
            move_obj = self.env['account.move']
            selling_price = record.selling_price * (6 / 100)
            vals = {
                'partner_id': record.partner_id.id,
                'move_type': 'out_invoice',
                "invoice_line_ids": [
                    Command.create({
                        'name': "6% of the selling price",
                        'quantity': 1,
                        'price_unit': selling_price,
                    })
                ],
            }
            move_obj.sudo().create(vals)
        return super(EstateProperty, self).action_sold()
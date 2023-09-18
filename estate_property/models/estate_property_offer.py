
from odoo import models, fields, api, _
import datetime
from odoo.exceptions import AccessError, UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property'
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validate', default=7)
    date_deadline = fields.Date(string="Deadline Date", compute='_compute_date_deadline', inverse="_inverse_validate")
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The offer price must be strictly postive')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = datetime.timedelta(days=offer.validity) + fields.Date.today()

    def _inverse_validate(self):
        day_count = (self.date_deadline - fields.Date.today()).days
        self.validity = day_count

    def action_accepted(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.partner_id = rec.partner_id
            rec.property_id.selling_price = rec.price
            rec.property_id.state = 'offer_accepted'

    def action_refused(self):
        self.status = 'refused'

    @api.model
    def create(self, vals):
        property_object = self.env['estate.property'].browse(vals['property_id'])
        property_object.write({'state' : 'offer_received'})
        for offer in property_object.offer_ids:
            if vals['price'] < offer.price:
                raise UserError(_("Your price is must be greather than %s", offer.price))
        return super(EstatePropertyOffer, self).create(vals)
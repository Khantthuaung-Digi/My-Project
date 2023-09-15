
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"
 
    name = fields.Char( required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date')
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living_area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden', store=True)
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection([('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', ' Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True, tracking=10)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    best_price = fields.Integer('Best Offer' , compute="_compute_best_price")
    total_area = fields.Integer('Total Area', compute="_compute_total_area")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be stricky postive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be stricky postive')
    ]
    
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price > 0:
                percentage_price = (record.expected_price / 100) * 90
                if record.selling_price < percentage_price:
                    raise ValidationError("Selling price should be 90% of the expected price.you must recuse expected price if you want to accept this offer")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        self.total_area = self.garden_area + self.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                for rec in record.offer_ids:
                    if record.best_price < rec.price:
                        record.best_price = rec.price
                    else:
                        record.best_price = record.best_price
            else:
                record.best_price = 0
        
    @api.onchange('garden')
    def _onchange_garden(self):
        for estate in self:
            if estate.garden == True:
                estate.garden_area = 10
                estate.garden_orientation = 'north'
            else:
                estate.garden_area = 0
                estate.garden_orientation = False
    
    def action_sold(self):
        for rec in self:
            if rec.state == 'canceled':
                raise UserError('Cancelled properties can not be sold')
            rec.state = 'sold'
            return True


    def action_cancel(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError('Sold properties can not be cancel')
            rec.state = 'canceled'
            return True

    @api.ondelete(at_uninstall=False)
    def _delete_sold_cancel(self):
        for rec in self:
            if rec.state in ('sold', 'canceled'):
                raise UserError("Can't delete an active user!")
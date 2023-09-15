
from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = "name asc"

    name = fields.Char( required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
        'Name must be unique!')
    ]
    
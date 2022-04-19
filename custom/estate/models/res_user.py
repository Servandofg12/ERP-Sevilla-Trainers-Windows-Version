from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    estate_property_ids = fields.One2many("estate.property", "user_id", string="Properties", domain=[("state", "in", ["new", "offer received"])])


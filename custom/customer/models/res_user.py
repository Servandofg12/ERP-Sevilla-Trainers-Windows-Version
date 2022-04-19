from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    customer_ids = fields.One2many("customer.customer", "user_id", string="Customer Data")


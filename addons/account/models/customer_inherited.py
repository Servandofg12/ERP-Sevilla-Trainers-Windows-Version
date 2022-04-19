from odoo import api, models, fields, _


class CustomerInherited(models.Model):
    _inherit = "customer.customer"

    
    account_move_ids = fields.One2many("account.move", "customer_id")

from odoo import api, models, fields, _


class EmployeeInherited(models.Model):
    _inherit = "hr.employee"

    
    account_move_ids = fields.One2many("account.move", "employee_id")
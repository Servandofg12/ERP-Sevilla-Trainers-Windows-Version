from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer()


    _sql_constraints = [
        ('check_name_uniq', 'UNIQUE(name)', 'The name must be unique.')
    ]

    def action_estate_property_tag(self):
        return {
            'name': ('Estate Property Tag'),
            'view_mode': 'tree,form',
            'res_model': 'estate.property.tag',
            'type': 'ir.actions.act_window',

        }
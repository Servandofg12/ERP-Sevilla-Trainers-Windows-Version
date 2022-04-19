from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence, name"
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order types.")

    estate_property_offers_ids = fields.Many2many("estate.property.offer", string="Offers")
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer")

    _sql_constraints = [
        ('check_name_uniq', 'UNIQUE(name)', 'The name must be unique.')
    ]

    @api.depends("property_ids")
    def _compute_offer(self):
        i = 0
        for record in self:
            lista_propiedades = record.property_ids
            for propiedad in lista_propiedades:
                lista_offers = propiedad.property_offer_ids
                i += len(lista_offers)
        record.offer_count = i



    def action_estate_property_type(self):
        return {
            'name': ('Estate Property Type'),
            'view_mode': 'tree,form',
            'res_model': 'estate.property.type',
            'type': 'ir.actions.act_window',

        }


from odoo import api, fields, models, exceptions
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"
    
    price = fields.Float()
    status = fields.Selection(
        string = 'Status',
        selection=[('accepted', 'Accepted'), ('refused','Refused')],
        help = "Type is used to separate",
        copy=False
    )
    customer_id = fields.Many2one('res.partner', string='Customer', index=True)
    estate_property_id = fields.Many2one("estate.property", string="Property")
    estate_property_type_id = fields.Many2one("estate.property.type", related="estate_property_id.property_type_id", store=True)#asi cogemos la tabla de type

    validity = fields.Integer()
    date_deadline = fields.Date(compute="_compute_date", inverse="_inverse_date", default=datetime.date.today())


    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'The price of the offer must be positive.')
    ]

    @api.depends("validity")
    def _compute_date(self):
        hoy = datetime.date.today()
        for record in self:
            fecha = hoy + relativedelta(days=record.validity)
            record.date_deadline = fecha

    def _inverse_date(self):
        hoy = datetime.date.today()
        for record in self:
            validity = record.date_deadline - hoy
            record.validity = validity.days


    @api.model
    def create(self, vals):
        if vals.get("estate_property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["estate_property_id"])
            # We check if the offer is higher than the existing offers
            if prop.property_offer_ids:
                max_offer = max(prop.mapped("property_offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise exceptions.UserError("The offer must be higher than %.2f" % max_offer)
            prop.state = "offer received"
        return super().create(vals)
    

    def action_confirm_status(self):
        for record in self:
            lista_offer = record.estate_property_id.property_offer_ids
            #print("Lista Offer:" + str(lista_offer))
            for offer in lista_offer:

                #print(str(offer.price)+"---"+str(offer.status))

                if (offer.status == "accepted") & (record != offer):
                    raise exceptions.UserError("There is already one offer accepted. First, refuse it and then accept another one.")
                else: 
                    print(offer.price)
                    print(record.estate_property_id.state != "offer aceppted")
                    if record.estate_property_id.state != "sold":
                        record.status = "accepted"
                        record.estate_property_id.selling_price = record.price
                        record.estate_property_id.partner_id = record.customer_id
                        record.estate_property_id.state = "offer aceppted"
                    else:
                        raise exceptions.UserError("The property is already sold.")
        return True

    def action_cancel_status(self):#tengo que ver que todos esten a refused para poner el selling price a 0 y poner el partner a None
        uno_aceptado = False
        for record in self:
            record.status = "refused"
            lista_offer = record.estate_property_id.property_offer_ids
            for offer in lista_offer:
                if not uno_aceptado:
                    if (offer.status == "accepted"):
                        uno_aceptado = True
            print(record.estate_property_id.state!="sold")
            print(not uno_aceptado)
            if not uno_aceptado & (record.estate_property_id.state!="sold"): 
                record.estate_property_id.selling_price = 0
                record.estate_property_id.partner_id = None
            else:
                if uno_aceptado & (record.estate_property_id.state!="sold"):
                    return True
                else:
                    raise exceptions.UserError("The property is already sold.")
        return True

    def action_estate_property_offer(self):
        return {
            'name': ('Estate Property Offer'),
            'view_mode': 'tree,form',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',

        }
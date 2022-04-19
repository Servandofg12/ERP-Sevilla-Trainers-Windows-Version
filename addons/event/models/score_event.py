from odoo import api, fields, models, exceptions, Command
from datetime import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class ScoreEvent(models.Model):
    _name = "score.event"
    _description = "Customer's score for an event participation."

    #Atributes of Score Event------------------------------------------------------------------------------------------------------
    score = fields.Float(required=True)

    #Relations between tables----------------------------------------------------------------------------------------------------------
    user_id = fields.Many2one('res.users', 'User', index=True, store=True, readonly=False, required=True)
    event_id = fields.Many2one("event.event", string="Event")


    #Constraints---------------------------------------------------------------------------------------------------------------------------
    _sql_constraints = [
        ('check_score_min', 'CHECK(score >= 0)', 'The score must be positive and greater than 0.'),
        ('check_score_max', 'CHECK(score <= 5)', 'The score must be lower than 5.'),
    ]


    @api.model
    def create(self, vals):
        today = datetime.today()
        event = self.env["event.event"].search([("id", "=", vals.get("event_id"))], limit=1)
        date_end = event.date_end
        if(today < date_end):
            raise UserError("The class isn't finished yet. You can't score an event that haven't finished.")

        scores = event.score_event_ids
        event_registration = event.registration_ids

        user = self.env["res.users"].search([("id", "=", vals.get("user_id"))], limit=1)
        username = user.name
        partner = self.env["res.partner"].search([("name", "=", username)], limit=1)

        is_registered = False
        if len(event_registration) > 0:
            for registration in event_registration:
                partner_who_voted = registration.partner_id

                if (partner_who_voted.id == partner.id):
                    is_registered = True

                if not is_registered:
                    raise UserError("That customer hasn't been registered for the event, so she can't score it.")
        else:
            raise UserError("That customer hasn't been registered for the event, so she can't score it.")

        for score in scores:
            customer_who_voted = score.user_id
            if (customer_who_voted.id == vals.get("user_id")):
                raise UserError("That customer has a score already.")
    
        return super().create(vals)
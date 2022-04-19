from odoo import api, fields, models
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class MonthlyReview(models.Model):
    _name = "monthly.review"
    _description = "Monthly review for the customers from Sevilla Trainers gym."
    _order = "date_made desc"

    #Atributes monthly review------------------------------------------------------------------------------------------------------
    new_weight = fields.Float(required=True)
    new_height = fields.Float(required=True)
    body_fat_percentage = fields.Float(required=True)
    body_mass_index = fields.Float(required=True)
    chest_measurement = fields.Float(required=True)
    weist_measurement = fields.Float(required=True)
    abdomen_measure = fields.Float(required=True)
    hips_measure = fields.Float(required=True)
    thighs_measure = fields.Float(required=True)
    arms_measure = fields.Float(required=True)
    date_made = fields.Date(default=datetime.date.today())

    #Relationship between tables-----------------------------------------------------------------------------------------------------------
    customer_id = fields.Many2one("customer.customer", string="Customer")


    #Constraints---------------------------------------------------------------------------------------------------------------------------
    _sql_constraints = [
        ('check_new_weight', 'CHECK(new_weight > 0)', 'The weight must be positive and greater than 0.'),
        ('check_new_height', 'CHECK(new_height > 0)', 'The height must be positive and greater than 0.'),
        ('check_body_fat_percentage', 'CHECK(body_fat_percentage > 0)', 'The body fat percentage must be positive and greater than 0.'),
        ('check_body_mass_index', 'CHECK(body_mass_index > 0)', 'The body mass index must be positive and greater than 0.'),
        ('check_chest_measurement', 'CHECK(chest_measurement > 0)', 'The chest measurement must be positive and greater than 0.'),
        ('check_weist_measurement', 'CHECK(weist_measurement > 0)', 'The weist measurement must be positive and greater than 0.'),
        ('check_abdomen_measure', 'CHECK(abdomen_measure > 0)', 'The abdomen measure must be positive and greater than 0.'),
        ('check_hips_measure', 'CHECK(hips_measure > 0)', 'The hips measure must be positive and greater than 0.'),
        ('check_thighs_measure', 'CHECK(thighs_measure > 0)', 'The thighs measure must be positive and greater than 0.'),
        ('check_arms_measure', 'CHECK(arms_measure > 0)', 'The arms measure must be positive and greater than 0.'),
    ]


    #On create ---------------------------------------------------------------------------------------------------------------------------
    @api.model
    def create(self, vals):
        today = datetime.date.today()
        customer = self.env["customer.customer"].browse(vals['customer_id'])
        first = True

        if len(customer.monthly_review_ids)>0:
            date_last_review = customer.monthly_review_ids[-1].date_made
            date_review_plus_month = date_last_review + relativedelta(months=1) - relativedelta(days=1)
            first = False

        if not first:
            if today < date_review_plus_month : 
                raise UserError("There isn't able to do a monthly review. You should wait until: " + str(date_last_review + relativedelta(months=1)))
            else:
            
                #Edit the actual weight and height
                self.env["customer.customer"].browse(vals['customer_id']).write(
                        {
                            "actual_weight": vals['new_weight'],
                            "actual_height": vals['new_height']
                        }
                    )
                
                #Create the monthly review
                result = super(MonthlyReview, self).create(vals)
                return result

        else:

            self.env["customer.customer"].browse(vals['customer_id']).write(
                        {
                            "actual_weight": vals['new_weight'],
                            "actual_height": vals['new_height']
                        }
                    )
                
            #Create the monthly review
            result = super(MonthlyReview, self).create(vals)
            return result
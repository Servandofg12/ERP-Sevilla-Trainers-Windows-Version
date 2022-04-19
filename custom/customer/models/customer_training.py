from odoo import api, fields, models
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class CustomerTraining(models.Model):#retocar el security 
    _name = "customer.training"
    _description = "Training for the customers from Sevilla Trainers gym."
    _order = "date_train desc"

    #Atributes training------------------------------------------------------------------------------------------------------
    date_train = fields.Date(default=datetime.date.today())
    name = fields.Char() 
    numb_turns = fields.Integer(default=1)
    machine_use = fields.Boolean()

    #Relationship between tables----------------------------------------------------------------------------------------------------------
    customer_id = fields.Many2one("customer.customer", string="Customer")
    training_machine_ids = fields.Many2many("training.machine", string="Machine")

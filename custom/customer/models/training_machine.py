from odoo import api, fields, models
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class TrainingMachines(models.Model):#retocar el security 
    _name = "training.machine"
    _description = "Machines for the trainings for the customers from Sevilla Trainers gym."
    _order = "name desc"

    #Atributes machine------------------------------------------------------------------------------------------------------
    name = fields.Char(required=True)

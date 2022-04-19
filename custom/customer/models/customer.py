from odoo import api, fields, models, exceptions, Command
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class Customer(models.Model):
    _name = "customer.customer"
    _description = "Customers for the Sevilla Trainers gym."
    _order = "name"

    #Atributes of customer------------------------------------------------------------------------------------------------------
    have_dni = fields.Boolean(default=True)
    dni = fields.Char()
    nie = fields.Char()
    name = fields.Char(required=True)
    surnames = fields.Char(required=True)
    birth_date = fields.Date(required=True)
    actual_weight = fields.Float(required=True)
    actual_height = fields.Float(required=True)
    registered = fields.Boolean(default=True)
    register_date = fields.Date(default=datetime.date.today())
    unsubscribe_date = fields.Date()
    phone = fields.Char(related="user_id.phone")
    email = fields.Char(related="user_id.email")
    address = fields.Char()
    ways_to_pay = fields.Selection(
        required = True,
        string = 'Way to pay',
        selection=[('transfer', 'Transfer'), ('in_hand','In Hand')],
        default = "transfer"
    )
    paid = fields.Boolean(default=True)
    payday = fields.Date(default=datetime.date.today() + relativedelta(months=1), readonly=True)
    goal = fields.Char()
    image_1920 = fields.Image(compute_sudo=True)

    #Relations between tables----------------------------------------------------------------------------------------------------------
    user_id = fields.Many2one('res.users', 'User', index=True, store=True, readonly=False)
    monthly_review_ids = fields.One2many("monthly.review", "customer_id", string="Monthly review")
    customer_training_ids = fields.One2many("customer.training", "customer_id", string="Trainings")
    #account_move_ids = fields.One2many("account.move", "customer_id")

    #Computed fields----------------------------------------------------------------------------------------------------------------------
    age = fields.Integer(compute="_compute_age")
    season_pass = fields.Selection(
        string = 'Type of season pass',
        selection=[('student', 'Student'), ('normal','Normal'), ('old_age','Old Age'), ('none','None')],
        compute = "_compute_season_pass_depending_on_age",
        store=True
    )
    season_pass_cost = fields.Float(compute="_compute_season_pass_cost")


    #Constraints---------------------------------------------------------------------------------------------------------------------------
    _sql_constraints = [
        ('check_actual_weight', 'CHECK(actual_weight > 0)', 'The weight must be positive and greater than 0.'),
        ('check_actual_height', 'CHECK(actual_height > 0)', 'The height must be positive and greater than 0.'),
        ('user_uniq', 'unique (user_id)', "This user is from other person. Please write or try another one."),
        ('dni_uniq', 'unique (dni)', "This DNI is from another person."),
        ('nie_uniq', 'unique (nie)', "This NIE is from another person."),
        #('unique_email', 'unique (email)', 'This email already exists.'),
    ]


    @api.constrains("birth_date")
    def _check_birth_date(self):
        for record in self:
            birth_date = record.birth_date
            hoy = datetime.date.today()

            if birth_date > hoy:
                raise ValidationError("The customer should have been born before today.")


    @api.constrains("name")
    def _check_name(self):
        for record in self:
            name = record.name

            name_pieces = name.split(" ")
            for piece in name_pieces:
                first = True
                if piece[0] != piece[0].upper():
                    raise ValidationError("The name mustn't start with a capital letter.")

                for letter in piece:
                    if re.match("[0-9]", letter):
                        raise ValidationError("The name mustn't contain numbers.")
            
                    if letter == letter.upper():
                        if (not first):
                            raise ValidationError("The name mustn't contain capital letters unless the first letter of the names.")
                    first = False
                

    @api.constrains("surnames")
    def _check_surnames(self):
        for record in self:
            surnames = record.surnames

            surname_pieces = surnames.split(" ")
            for piece in surname_pieces:
                first = True
                if piece[0] != piece[0].upper():
                    raise ValidationError("The surnames mustn't start with a capital letter.")

                for letter in piece:
                    if re.match("[0-9]", letter):
                        raise ValidationError("The surnames mustn't contain numbers.")
            
                    if letter == letter.upper():
                        if (not first):
                            raise ValidationError("The surnames mustn't contain capital letters unless the first letter of the surnames.")
                    first = False


    @api.constrains("user_id")
    def _check_user_id(self):
        for record in self:
            user = record.user_id

            if user:

                self._cr.execute('select count(*) from hr_employee where user_id = %s', (user.id,))
                data = self._cr.dictfetchall()

                if data[0]['count'] > 0:
                    raise ValidationError("This user is from other person. Please write or try another one.")



    #Computed fields functions-------------------------------------------------------------------------------------------------------------
    @api.depends("birth_date", "age")
    def _compute_age(self):
        for record in self:
            birth_date = record.birth_date
            today = datetime.date.today()

            if birth_date:

                if today.month < birth_date.month:
                    record.age = today.year - birth_date.year - 1

                elif today.month > birth_date.month:
                    record.age = today.year - birth_date.year

                else:
                    if today.day >= birth_date.day:
                        record.age = today.year - birth_date.year

                    else:
                        record.age = today.year - birth_date.year -1
                
                if record.age < 14:
                        raise ValidationError("To register the customer should be 14 or older.")


            else:
                record.age = 0

            if record.age < 0:
                record.age = 0



    @api.depends("age")
    def _compute_season_pass_depending_on_age(self):
        for record in self:
            age = record.age

            if age > 0:
                if age <= 21:
                    record.season_pass = "student"

                elif age <= 59:
                    record.season_pass = "normal"

                else:
                    record.season_pass = "old_age"

            else:
                record.season_pass = "none"



    @api.depends("season_pass", "ways_to_pay")
    def _compute_season_pass_cost(self):
        for record in self:
            season_pass = record.season_pass
            way_to_pay = record.ways_to_pay
            in_hand = way_to_pay == "in_hand"

            if season_pass: 

                if season_pass == "student":
                    if in_hand:
                        record.season_pass_cost = 20.99
                    else:
                        record.season_pass_cost = 23.99

                elif season_pass == "normal":
                    if in_hand:
                        record.season_pass_cost = 30.99
                    else:
                        record.season_pass_cost = 33.99

                elif season_pass == "old_age":
                    if in_hand:
                        record.season_pass_cost = 24.99
                    else:
                        record.season_pass_cost = 27.99
                
                else:
                    record.season_pass_cost = 0.0
            
            else:
                record.season_pass_cost = 0.0


    #Actions-------------------------------------------------------------------------------------------------------------

    def action_register(self):
        for record in self:
            if record.registered == True:
                raise exceptions.UserError("She is already registered.")
            else:
                record.registered = True
                record.register_date = datetime.date.today()
                record.unsubscribe_date = None
                record.payday = datetime.date.today() + relativedelta(months=1)
        return True

    def action_unsubscribe(self):
        for record in self:
            if record.registered == False:
                raise exceptions.UserError("She is already unsubscribed.")
            else:
                record.registered = False
                record.unsubscribe_date = datetime.date.today()
        return True

    def action_monthly_payment(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for record in self:
            partner = self.env["res.partner"].search([("name", "=", record.user_id.name)], limit=1)

            if(record.registered):
                next_payday = record.payday + relativedelta(months=1)
                record.payday = next_payday

                account_move = self.env["account.move"].create(
                    {
                        "name": "Monthly payment of customer " + str(record.name) + " " + str(len(record.account_move_ids)+1),
                        "partner_id": partner,
                        "move_type": "out_invoice",
                        "journal_id": journal.id,
                        "customer_id": record.id,
                        "invoice_line_ids": 
                            Command.create(
                                {
                                    "name": record.name,
                                    "quantity": 1.0,
                                    "price_unit": record.season_pass_cost,
                                })
                    }
                )
                
                account_move.action_post()#to post it
                account_move.action_register_payment()#to make it paid
            
            else:
                raise UserError("This customer isn't registered.")



    




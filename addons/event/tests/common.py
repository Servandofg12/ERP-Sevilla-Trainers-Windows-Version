# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import timedelta, datetime
from odoo import fields
from odoo.addons.mail.tests.common import mail_new_test_user
from odoo.tests import common
from dateutil.relativedelta import relativedelta

@common.tagged("eventScore", "post_install")
class TestEventCommon(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestEventCommon, cls).setUpClass()

        # Test users to use through the various tests
        cls.user_portal = mail_new_test_user(
            cls.env, login='portal_test',
            name='Patrick Portal', email='patrick.portal@test.example.com',
            notification_type='email', company_id=cls.env.ref("base.main_company").id,
            groups='base.group_portal')
        cls.user_employee = mail_new_test_user(
            cls.env, login='user_employee',
            name='Eglantine Employee', email='eglantine.employee@test.example.com',
            tz='Europe/Brussels', notification_type='inbox',
            company_id=cls.env.ref("base.main_company").id,
            groups='base.group_user',
        )
        cls.user_eventregistrationdesk = mail_new_test_user(
            cls.env, login='user_eventregistrationdesk',
            name='Ursule EventRegistration', email='ursule.eventregistration@test.example.com',
            tz='Europe/Brussels', notification_type='inbox',
            company_id=cls.env.ref("base.main_company").id,
            groups='base.group_user,event.group_event_registration_desk',
        )
        cls.user_eventuser = mail_new_test_user(
            cls.env, login='user_eventuser',
            name='Ursule EventUser', email='ursule.eventuser@test.example.com',
            tz='Europe/Brussels', notification_type='inbox',
            company_id=cls.env.ref("base.main_company").id,
            groups='base.group_user,event.group_event_user',
        )
        cls.user_eventmanager = mail_new_test_user(
            cls.env, login='user_eventmanager',
            name='Martine EventManager', email='martine.eventmanager@test.example.com',
            tz='Europe/Brussels', notification_type='inbox',
            company_id=cls.env.ref("base.main_company").id,
            groups='base.group_user,event.group_event_manager',
        )

        cls.event_customer = cls.env['res.partner'].create({
            'name': 'Constantin Customer',
            'email': 'constantin@test.example.com',
            'country_id': cls.env.ref('base.be').id,
            'phone': '0485112233',
            'mobile': False,
        })
        cls.event_customer2 = cls.env['res.partner'].create({
            'name': 'Constantin Customer 2',
            'email': 'constantin2@test.example.com',
            'country_id': cls.env.ref('base.be').id,
            'phone': '0456987654',
            'mobile': '0456654321',
        })

        cls.event_type_complex = cls.env['event.type'].create({
            'name': 'Update Type',
            'auto_confirm': True,
            'has_seats_limitation': True,
            'seats_max': 30,
            'default_timezone': 'Europe/Paris',
            'event_type_ticket_ids': [(0, 0, {
                    'name': 'First Ticket',
                }), (0, 0, {
                    'name': 'Second Ticket',
                })
            ],
            'event_type_mail_ids': [
                (0, 0, {  # right at subscription
                    'interval_unit': 'now',
                    'interval_type': 'after_sub',
                    'template_ref': 'mail.template,%i' % cls.env['ir.model.data']._xmlid_to_res_id('event.event_subscription')}),
                (0, 0, {  # 1 days before event
                    'interval_nbr': 1,
                    'interval_unit': 'days',
                    'interval_type': 'before_event',
                    'template_ref': 'mail.template,%i' % cls.env['ir.model.data']._xmlid_to_res_id('event.event_reminder')}),
            ],
        })
        cls.event_0 = cls.env['event.event'].create({
            'name': 'TestEvent',
            'auto_confirm': True,
            'date_begin': fields.Datetime.to_string(datetime.today() + timedelta(days=1)),
            'date_end': fields.Datetime.to_string(datetime.today() + timedelta(days=15)),
            'date_tz': 'Europe/Brussels',
        })

        cls.event_1 = cls.env['event.event'].create({
            'name': 'TestEvent',
            'auto_confirm': True,
            'date_begin': fields.Datetime.to_string(datetime.today() - timedelta(days=1)),
            'date_end': fields.Datetime.to_string(datetime.today() - timedelta(days=1)),
            'date_tz': 'Europe/Brussels',
        })

        # set country in order to format Belgian numbers
        cls.event_0.company_id.write({'country_id': cls.env.ref('base.be').id})

        cls.user_without_image = cls.env['res.users'].create({
            'name': 'Marc Demo',
            'email': 'mark.brown23@example.com',
            'image_1920': False,
            'login': 'demo_1',
            'password': 'demo_123'
        })

        today = datetime.today()
        normal_date = today - relativedelta(years=23)
        cls.customer = cls.env['customer.customer'].create(
                {
                    'have_dni': True, 
                    'dni': "66727211S",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': normal_date,
                    'actual_weight': 65.0,
                    'actual_height': 1.75,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to become more confidence.",
                    'user_id': cls.user_without_image.id
                })

    @classmethod
    def _create_registrations(cls, event, reg_count):
        # create some registrations
        registrations = cls.env['event.registration'].create([{
            'event_id': event.id,
            'name': 'Test Registration %s' % x,
            'email': '_test_reg_%s@example.com' % x,
            'phone': '04560000%s%s' % (x, x),
        } for x in range(0, reg_count)])
        return registrations




#MY TESTS ------------------------------------------------------------------------------------------------------------------
    def test_p_01_incorrect_score(self):
        print("\n")
        print("FIRST TEST")

        try:
            self.env['score.event'].create(
                    {
                        'score': 4.5,
                        'user_id': self.event_customer.id, 
                        'event_id': self.event_1.id
                    })
        except:
            print("It brings an Usererror: That customer hasn't been registered for the event, so she can't score it.")


    def test_p_02_correct_score(self):
        print("\n")
        print("SECOND TEST")
    
        username = self.customer.user_id.name
        partner = self.env["res.partner"].search([("name", "=", username)], limit=1)

        self.env['event.registration'].create({
            'event_id': self.event_1.id,
            'name': 'Test Registration',
            'email': '_test_reg_@example.com',
            'phone': '04560000',
            'partner_id': partner.id
            })
            
        registration = self.event_1.registration_ids
        print("Registration: " +str(len(registration)))
        for registro in registration:
            print("Partner that is registered: " +str(registro.partner_id.name))

        score_event = self.env['score.event'].create(
                    {
                        'score': 4.5,
                        'user_id': self.customer.user_id.id, 
                        'event_id': self.event_1.id
                    })

        print("SCORE: " + str(score_event.score))
        print("USER: " + str(score_event.user_id.name))
        print("EVENT: " + str(score_event.event_id.name))


    def test_p_03_double_score(self):
        print("\n")
        print("SECOND TEST")

        try:
            username = self.customer.user_id.name
            partner = self.env["res.partner"].search([("name", "=", username)], limit=1)

            self.env['event.registration'].create({
                'event_id': self.event_1.id,
                'name': 'Test Registration',
                'email': '_test_reg_@example.com',
                'phone': '04560000',
                'partner_id': partner.id
                })
                
            registration = self.event_1.registration_ids
            print("Registration: " +str(len(registration)))
            for registro in registration:
                print("Partner that is registered: " +str(registro.partner_id.name))

            score_event = self.env['score.event'].create(
                        {
                            'score': 4.5,
                            'user_id': self.customer.user_id.id, 
                            'event_id': self.event_1.id
                        })

            print("FIRST SCORE")
            print("SCORE: " + str(score_event.score))
            print("USER: " + str(score_event.user_id.name))
            print("EVENT: " + str(score_event.event_id.name))
            print("TOTAL SCORES: " + str(len(self.event_1.score_event_ids)))

            score_event_2 = self.env['score.event'].create(
                        {
                            'score': 4.5,
                            'user_id': self.customer.user_id.id, 
                            'event_id': self.event_1.id
                        })
            print("SECOND SCORE")
            print("SCORE: " + str(score_event.score))
            print("USER: " + str(score_event.user_id.name))
            print("EVENT: " + str(score_event.event_id.name))
            print("TOTAL SCORES: " + str(len(self.event_1.score_event_ids)))
        
        except:
            print("It brings an Usererror: That customer has already scored the event, so she can't score it again.")
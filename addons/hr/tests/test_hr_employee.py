# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import Form
from odoo.addons.hr.tests.common import TestHrCommon
from odoo.tests import tagged
import datetime
from dateutil.relativedelta import relativedelta

@tagged('post_install', 'employee')
class TestHrEmployee(TestHrCommon):

    def setUp(self):
        super().setUp()
        self.user_without_image = self.env['res.users'].create({
            'name': 'Marc Demo',
            'email': 'mark.brown23@example.com',
            'image_1920': False,
            'login': 'demo_1',
            'password': 'demo_123'
        })
        self.employee_without_image = self.env['hr.employee'].create({
            'user_id': self.user_without_image.id,
            'image_1920': False
        })

        #FOR REGISTER AND UNSUBSCRIBE FUNCTIONALITIES ----------------------
        self.user_without_image_2 = self.env['res.users'].create([{
            'name': 'Prueba',
            'email': 'prueba23@example.com',
            'image_1920': False,
            'login': 'prueba_1',
            'password': 'prueba_123'
        },{
            'name': 'Prueba2',
            'email': 'prueba23333@example.com',
            'image_1920': False,
            'login': 'prueba_2',
            'password': 'prueba_123'
        },{
            'name': 'Prueba3',
            'email': 'prueba3333@example.com',
            'image_1920': False,
            'login': 'prueba_3',
            'password': 'prueba_123'
        },{
            'name': 'Prueba4',
            'email': 'prueba4444@example.com',
            'image_1920': False,
            'login': 'prueba_4',
            'password': 'prueba_123'
        }])

        self.employee_without_image_2 = self.env['hr.employee'].create([{
            'user_id': self.user_without_image_2[0].id,
            'image_1920': False,
        },{
            'user_id': self.user_without_image_2[1].id,
            'image_1920': False,
            'registered': False,
            'unsubscribe_date': datetime.date.today() - relativedelta(months=2)
        }])

        normal_date = datetime.date.today() - relativedelta(years=23)

        self.customer = self.env['customer.customer'].create([
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
                    'user_id': self.user_without_image_2[2].id
                },
                {
                    'have_dni': True, 
                    'dni': "66727240W",
                    'name': "Hola",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': normal_date,
                    'actual_weight': 65.0,
                    'actual_height': 1.75,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to become more confidence.",
                    'user_id': self.user_without_image_2[3].id,
                    'registered': False,
                    'unsubscribe_date': datetime.date.today() - relativedelta(months=2)
                }]
            )





    def test_employee_resource(self):
        _tz = 'UTC'
        self.res_users_hr_officer.company_id.resource_calendar_id.tz = _tz
        Employee = self.env['hr.employee'].with_user(self.res_users_hr_officer)
        employee_form = Form(Employee)
        employee_form.name = 'Raoul Grosbedon'
        employee_form.work_email = 'raoul@example.com'
        employee = employee_form.save()
        self.assertEqual(employee.tz, _tz)

    def test_employee_from_user(self):
        _tz = 'Pacific/Apia'
        _tz2 = 'America/Tijuana'
        self.res_users_hr_officer.company_id.resource_calendar_id.tz = _tz
        self.res_users_hr_officer.tz = _tz2
        Employee = self.env['hr.employee'].with_user(self.res_users_hr_officer)
        employee_form = Form(Employee)
        employee_form.name = 'Raoul Grosbedon'
        employee_form.work_email = 'raoul@example.com'
        employee_form.user_id = self.res_users_hr_officer
        employee = employee_form.save()
        self.assertEqual(employee.name, 'Raoul Grosbedon')
        self.assertEqual(employee.work_email, self.res_users_hr_officer.email)
        self.assertEqual(employee.tz, self.res_users_hr_officer.tz)

    '''def test_employee_from_user_tz_no_reset(self):
        _tz = 'Pacific/Apia'
        self.res_users_hr_officer.tz = False
        Employee = self.env['hr.employee'].with_user(self.res_users_hr_officer)
        employee_form = Form(Employee)
        employee_form.name = 'Raoul Grosbedon'
        employee_form.work_email = 'raoul@example.com'
        employee_form.tz = _tz
        employee_form.user_id = self.res_users_hr_officer
        employee = employee_form.save()
        self.assertEqual(employee.name, 'Raoul Grosbedon')
        self.assertEqual(employee.work_email, self.res_users_hr_officer.email)
        self.assertEqual(employee.tz, _tz)'''

    def test_employee_has_avatar_even_if_it_has_no_image(self):
        self.assertTrue(self.employee_without_image.avatar_128)
        self.assertTrue(self.employee_without_image.avatar_256)
        self.assertTrue(self.employee_without_image.avatar_512)
        self.assertTrue(self.employee_without_image.avatar_1024)
        self.assertTrue(self.employee_without_image.avatar_1920)

    def test_employee_has_same_avatar_as_corresponding_user(self):
        self.assertEqual(self.employee_without_image.avatar_1920, self.user_without_image.avatar_1920)



    #TESTS FOR REGISTER AND UNSUBSCRIBE FUNCTIONALITIES -----------------------------------------------------------------------

    def test_p_1_register_action(self):
        print("FIRST TEST")
        print("\n")
        #Solo el segundo esta dado de baja ([1]), por lo tanto, el primero ([0]) esta dado de alta.
        print("BEFORE: Registered: " + str(self.employee_without_image_2[1].registered) + " - Unsubscribed date: " + str(self.employee_without_image_2[1].unsubscribe_date))
        print("\n")
        self.employee_without_image_2[1].action_register()
        print("AFTER: Registered: " + str(self.employee_without_image_2[1].registered) + " - Register date: " + str(self.employee_without_image_2[1].register_date))
        print("\n")
        var = self.assertRecordValues(self.employee_without_image_2,[
            {'name': 'Prueba', 'registered': True},
            {'name': 'Prueba2', 'registered': True}
        ])

        return var


    def test_p_2_register_action_wrong(self):
        print("SECOND TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.employee_without_image_2[0].registered) + " - Unsubscribed date: " + str(self.employee_without_image_2[0].unsubscribe_date))
        print("\n")
        try:
            self.employee_without_image_2[0].action_register()
            print("AFTER: Registered: " + str(self.employee_without_image_2[0].registered) + " - Register date: " + str(self.employee_without_image_2[0].register_date))
            print("\n")
            var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'registered': True},
                {'name': 'Prueba2', 'registered': False}
            ])
            return var
        except:
            print("She's already registered so it gives an UserError exception")
            print("\n")
            var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'registered': True},
                {'name': 'Prueba2', 'registered': False}
            ])
            return var


    def test_p_3_unsubscribe_action(self):
        print("THIRD TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.employee_without_image_2[0].registered) + " - Unsubscribed date: " + str(self.employee_without_image_2[0].unsubscribe_date))
        print("\n")

        self.employee_without_image_2[0].action_unsubscribe()

        print("AFTER: Registered: " + str(self.employee_without_image_2[0].registered) + " - Unsubscribed date: " + str(self.employee_without_image_2[0].unsubscribe_date))
        print("\n")
        var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'registered': False},
                {'name': 'Prueba2', 'registered': False}
                ])
        return var


    def test_p_4_unsubscribe_action_wrong(self):
        print("FOURTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.employee_without_image_2[1].registered) + " - Unsubscribed date: " + str(self.employee_without_image_2[1].unsubscribe_date))
        print("\n")
        try:
            self.employee_without_image_2[1].action_unsubscribe()
            print("AFTER: Registered: " + str(self.employee_without_image_2[1].registered) + " - Unsubscribed date: " + str(self.employee_without_image_2[1].unsubscribe_date))
            print("\n")
            var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'registered': True},
                {'name': 'Prueba2', 'registered': False}
            ])
            return var
        except:
            print("She's already unsubscribed so it gives an UserError exception")
            print("\n")
            var = self.assertRecordValues(self.employee_without_image_2,[
                {'name': 'Prueba', 'registered': True},
                {'name': 'Prueba2', 'registered': False}
            ])
            return var


    #LOGIN TEST ---------------------------------------------------------------------------------------------------------------

    def test_p_5_create_user_with_the_same_other_username(self):
        print("FIFTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: User: " + str(self.employee_without_image_2[0].user_id.name))
        print("\n")
        try:
            self.employee_without_image_wrong = self.env['hr.employee'].create({
            'user_id': self.user_without_image_2[0].id,
            'image_1920': False,
        })
        except:
            print("That username already exists. Try with another one.")
            print("\n")
            var = True
            return var


    def test_p_6_create_user_with_the_same_username_as_employee(self):
        print("SIXTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: User employee: " + str(self.employee_without_image_2[0].user_id.name))
        print("\n")
        try:
            normal_date = datetime.date.today() - relativedelta(years=23)

            self.customer = self.env['customer.customer'].create([
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
                    'goal': "Quiero ganar confianza en mí misma.",
                    'user_id': self.employee_without_image_2[0].user_id.id
                }
            ])
        except:
            print("That username already exists. Try with another one.")
            print("\n")
            var = True
            return var


    def test_p_7_create_user_with_the_same_username_as_customer(self):
        print("SEVENTH TEST")
        print("\n")

        print("BEFORE: User customer: " + str(self.customer[0].user_id.login))
        print("\n")
        try:
            self.employee_without_image_2 = self.env['hr.employee'].create({
            'name': 'Prueba',
            'user_id': self.customer[0].user_id.id,
            'image_1920': False,
        })
        except:
            print("That username already exists. Try with another one.")
            print("\n")
            var = True
            return var

    #TEST EDIT DATA ---------------------------------------------------------------------------------------------------------------

    def test_p_8_edit_employee_data(self):
        print("EIGHTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Name employee: " + str(self.employee_without_image_2[0].name))
        print("\n")

        self.employee_without_image_2_2 = self.employee_without_image_2[0].write({
            'name': 'Jose Maria'
        })
        
        print("AFTER: Name employee: " + str(self.employee_without_image_2[0].name))
        print("\n")
        var = self.assertEqual(self.employee_without_image_2[0].name, 'Jose Maria')
        return var


    #TEST FOR MONTHLY PAYMENT FUNCTIONALITY ---------------------------------------------------------------------

    def test_p_9_one_monthly_payment_for_customer(self):
        print("NINETH TEST")
        print("\n")
        first_payday = self.customer[0].payday
        print("BEFORE: Payday: " + str(self.customer[0].payday))
        print("\n")

        self.customer[0].action_monthly_payment()
        print("AFTER: Payday: " + str(self.customer[0].payday))
        account_move = self.env["account.move"].search([("customer_id", "=", self.customer[0].id)], limit=1)
        print(account_move.name)
        print("\n")

        var = self.assertEqual(self.customer[0].payday, first_payday + relativedelta(months=1))
        var2 = self.assertEqual(account_move.name, "Monthly payment of customer Hola 1")
        result = var and var2

        return result


    def test_p_10_one_monthly_payment_for_an_unsubscribed_customer(self):
        print("TENTH TEST")
        print("\n")
        first_payday = self.customer[1].payday
        print("BEFORE: Payday: " + str(self.customer[1].payday))
        print("\n")

        try:
            self.customer[1].action_monthly_payment()
        except: 
            print("AFTER: Payday: " + str(self.customer[1].payday))
            print("\n")

        var = self.assertEqual(first_payday, self.customer[1].payday)

        return var

    
    def test_p_11_one_monthly_payment_for_employee(self):
        print("ELEVENTH TEST")
        print("\n")
        first_payday = self.employee_without_image_2[0].payday
        print("BEFORE: Payday: " + str(self.employee_without_image_2[0].payday))
        print("\n")

        self.employee_without_image_2[0].action_monthly_payment()
        print("AFTER: Payday: " + str(self.employee_without_image_2[0].payday))
        print("\n")

        var = self.assertEqual(self.employee_without_image_2[0].payday, first_payday + relativedelta(months=1))

        return var

    
    def test_p_12_one_monthly_payment_for_an_unsubscribed_customer(self):
        print("TWELFTH TEST")
        print("\n")
        first_payday = self.employee_without_image_2[1].payday
        print("BEFORE: Payday: " + str(self.employee_without_image_2[1].payday))
        print("\n")

        try:
            self.employee_without_image_2[1].action_monthly_payment()
        except: 
            print("AFTER: Payday: " + str(self.employee_without_image_2[1].payday))
            print("\n")

        var = self.assertEqual(first_payday, self.employee_without_image_2[1].payday)

        return var
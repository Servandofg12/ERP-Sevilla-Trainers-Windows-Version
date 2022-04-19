from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
import datetime
from dateutil.relativedelta import relativedelta

@tagged('customer', 'post_install')
class CustomerTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(CustomerTestCase, cls).setUpClass()
        print("\n")
        print("SETUP FOR CUSTOMERS")
        print("\n")

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.

        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        normal_date = today - relativedelta(years=23)

        cls.customers = cls.env['customer.customer'].create([
            {
                'have_dni': True, 
                'dni': "66727272Z",
                'name': "Hello",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': normal_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "transfer",
                'goal': "I want to gain muscle mass"
            },
            {
                'have_dni': True, 
                'dni': "66727272A",
                'name': "Hello",
                'surnames': "Example Example",
                'birth_date': student_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "in_hand",
                'goal': "I want to gain muscle mass",
                'registered': False,
                'unsubscribe_date': today - relativedelta(months=2)
            }
        ])

        cls.machines = cls.env['training.machine'].create([
            {
                'name': "Squats"
            },
            {
                'name': "Chest/Back"
            }
        ])


    def test_p_01_correct_customer(self):
        print("\n")
        print("FIRST TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        normal_date = today - relativedelta(years=23)

        self.customers = self.env['customer.customer'].create([
            {
                'have_dni': True, 
                'dni': "72727272Z",
                'name': "Pepe",
                'surnames': "Ejemplo Ejemplo",
                'birth_date': normal_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "transfer",
                'goal': "I want to gain muscle mass"
            },
            {
                'have_dni': True, 
                'dni': "72727272A",
                'name': "Mariano",
                'surnames': "Example Example",
                'birth_date': student_date,
                'actual_weight': 70.0,
                'actual_height': 1.80,
                'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                'ways_to_pay': "in_hand",
                'goal': "I want to gain muscle mass"
            }
        ])

        print("¿Registered? " + str(self.customers[0].registered))
        print("Full name: " + str(self.customers[0].name) + " " + str(self.customers[0].surnames))
        print("Age: " + str(self.customers[0].age))
        print("Season pass: " + str(self.customers[0].season_pass))
        print("Season pass cost: " + str(self.customers[0].season_pass_cost))
        print("\n")

        print("¿Registered? " + str(self.customers[1].registered))
        print("Full name: " + str(self.customers[1].name) + " " + str(self.customers[1].surnames))
        print("Age: " + str(self.customers[1].age))
        print("Season pass: " + str(self.customers[1].season_pass))
        print("Season pass cost: " + str(self.customers[1].season_pass_cost))
        print("\n")

        var = self.assertEqual(self.customers[0].registered, True)
        var2 = self.assertEqual(self.customers[1].registered, True)
        result = var and var2
        return result


    def test_p_02_customer_name_with_wrong_capital_letter(self):
        print("\n")
        print("SECOND TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "HoLa",#falla aqui
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                }])
        except:
            print("The name contains capital letters and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    def test_p_03_customer_name_with_number(self):
        print("\n")
        print("THIRD TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "H9La",#falla aqui
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                }])
        except:
            print("The name contains a number and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    def test_p_04_customer_surname_with_wrong_capital_letter(self):
        print("\n")
        print("FOURTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "EjemPlo EjemPlo",#falla aqui
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                }])
        except:
            print("The surnames contains capital letters and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    def test_p_05_customer_surname_with_number(self):
        print("\n")
        print("FIFTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo 2Ejemplo",#falla aqui
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                }])
        except:
            print("The surnames contains a number letters and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    def test_p_06_customer_age_under_14(self):
        print("\n")
        print("SIXTH TEST")
        today = datetime.date.today()
        fecha_nac = today - relativedelta(years=10)
        self.customers = self.env['customer.customer']
        try:
            var = self.assertEqual(False, True)
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,#falla aqui
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                }])
            return var
        except:
            print("The age is under 14 and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var


    def test_p_07_customer_with_negative_weight(self):
        print("\n")
        print("SEVENTH TEST")
        today = datetime.date.today()
        fecha_nac = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,
                    'actual_weight': -200.0,#falla aqui
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                }])
        except:
            print("The weight can't be negative and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var
            
        return False

        
    def test_p_08_customer_with_negative_height(self):
        print("\n")
        print("EIGHTH TEST")
        today = datetime.date.today()
        fecha_nac = today - relativedelta(years=19)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,
                    'actual_weight': 70.0,
                    'actual_height': -1.80,#falla aqui
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                }])
        except:
            print("The height can't be negative and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    def test_p_09_customer_with_birth_date_in_the_future(self):
        print("\n")
        print("NINETH TEST")
        today = datetime.date.today()
        fecha_nac = today + relativedelta(years=1)
        self.customers = self.env['customer.customer']
        try:
            self.customers.create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': fecha_nac,#falla aqui
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                }])
        except:
            print("The birth date can't be in the future and it can't create the customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    def test_p_10_two_customers_with_the_same_DNI(self):
        print("\n")
        print("TENTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        normal_date = today - relativedelta(years=23)

        try:
            self.customers = self.env['customer.customer'].create([
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': normal_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                },
                {
                    'have_dni': True, 
                    'dni': "72727272Z",
                    'name': "Hello",
                    'surnames': "Example Example",
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "in_hand",
                    'goal': "I want to gain muscle mass"
                }
            ])
        except:
            print("Both customers have the same DNI and it can't create the second customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False

    
    def test_p_11_wo_customers_with_the_same_NIE(self):
        print("\n")
        print("ELEVENTH TEST")
        today = datetime.date.today()
        student_date = today - relativedelta(years=19)
        normal_date = today - relativedelta(years=23)

        try:
            self.customers = self.env['customer.customer'].create([
                {
                    'have_dni': False, 
                    'nie': "72727272Z",
                    'name': "Hello",
                    'surnames': "Ejemplo Ejemplo",
                    'birth_date': normal_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "transfer",
                    'goal': "I want to gain muscle mass"
                },
                {
                    'have_dni': False, 
                    'nie': "72727272Z",
                    'name': "Hello",
                    'surnames': "Example Example",
                    'birth_date': student_date,
                    'actual_weight': 70.0,
                    'actual_height': 1.80,
                    'address': "C/ Niña de la Alfalfa 3, Esc 33, 3º B",
                    'ways_to_pay': "in_hand",
                    'goal': "I want to gain muscle mass"
                }
            ])
        except:
            print("Both customers have the same NIE and it can't create the second customer")
            print("\n")
            var = self.assertEqual(False, False)
            return var

        return False


    #TESTS FOR REGISTER AND UNSUBSCRIBE FUNCTIONALITY -----------------------------------------------------------------------

    def test_p_12_register_action(self):
        print("TWELFTH TEST")
        print("\n")
        #Solo el segundo esta dado de baja ([1]), por lo tanto, el primero ([0]) esta dado de alta.
        print("BEFORE: Registered: " + str(self.customers[1].registered) + " - Unsubscribe date: " + str(self.customers[1].unsubscribe_date))
        print("\n")
        self.customers[1].action_register()
        print("AFTER: Registered: " + str(self.customers[1].registered) + " - Register date: " + str(self.customers[1].register_date))
        print("\n")
        var = self.assertRecordValues(self.customers,[
            {'name': 'Hello', 'registered': True},
            {'name': 'Hello', 'registered': True}
        ])

        return var


    def test_p_13_try_to_register_action(self):
        print("THIRTEENTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.customers[0].registered) + " - Unsubscribe date: " + str(self.customers[0].unsubscribe_date))
        print("\n")
        try:
            self.customers[0].action_register()
            print("AFTER: Registered: " + str(self.customers[0].registered) + " - Register date: " + str(self.customers[0].register_date))
            print("\n")
            var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var
        except:
            print("She's already registered so it gives an UserError exception")
            print("\n")
            var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var


    def test_p_14_unsubscribe_action(self):
        print("FOURTEENTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.customers[0].registered) + " - Unsubscribe date: " + str(self.customers[0].unsubscribe_date))
        print("\n")

        self.customers[0].action_unsubscribe()

        print("AFTER: Registered: " + str(self.customers[0].registered) + " - Unsubscribe date: " + str(self.customers[0].unsubscribe_date))
        print("\n")
        var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': False},
                {'name': 'Hello', 'registered': False}
                ])
        return var


    def test_p_15_try_unsubscribe_action(self):
        print("FIFTEENTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Registered: " + str(self.customers[1].registered) + " - Unsubscribe date: " + str(self.customers[1].unsubscribe_date))
        print("\n")
        try:
            self.customers[1].action_unsubscribe()
            print("AFTER: Registered: " + str(self.customers[1].registered) + " - Unsubscribe date: " + str(self.customers[1].unsubscribe_date))
            print("\n")
            var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var
        except:
            print("She's already unsubscribed so it gives an UserError exception")
            print("\n")
            var = self.assertRecordValues(self.customers,[
                {'name': 'Hello', 'registered': True},
                {'name': 'Hello', 'registered': False}
            ])
            return var


    #TESTS FOR THE MONTHLY REVIEW FUNCTIONALITY -----------------------------------------------------------------------

    def test_p_16_correct_monthly_review(self):
        print("SIXTEENTH TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("Customer's weight: " + str(self.customers[0].actual_weight))
        print("Customer's height: " + str(self.customers[0].actual_height))
        print("\n")
        self.review = self.env['monthly.review']
        self.review.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.customers[0].id
                }])

        print("AFTER: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("Customer's weight: " + str(self.customers[0].actual_weight))
        print("Customer's height: " + str(self.customers[0].actual_height))
        print("\n")

        var = self.assertEqual(1, len(self.customers[0].monthly_review_ids))
        return var


    def test_p_17_wrong_monthly_review_same_date(self):
        print("SEVENTEENTH TEST")
        print("\n")

        self.review = self.env['monthly.review']
        self.review.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.customers[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")

        try:
            print("Trying to add another review with the same date...")
            self.wrong_review = self.env['monthly.review']
            self.wrong_review.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.customers[0].id
                }])
        except:
            print("It goes wrong because you have to wait a month to do another review.")
            print("AFTER: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
            print("\n")

            var = self.assertEqual(1, len(self.customers[0].monthly_review_ids))
            return var
        
    def test_p_18_wrong_monthly_review_in_the_same_month(self):
        print("EIGHTEENTH TEST")
        print("\n")

        self.review = self.env['monthly.review']
        self.review.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.customers[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")

        try:
            print("Trying to add another review 29 days later...")
            self.wrong_review = self.env['monthly.review']
            self.wrong_review.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today() + relativedelta(months=1) - relativedelta(days=1),
                    'customer_id': self.customers[0].id
                }])
        except:
            print("It goes wrong because you have to wait an entirely month.")
            print("AFTER: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
            print("\n")

            var = self.assertEqual(1, len(self.customers[0].monthly_review_ids))
            return var


    def test_p_19_two_monthly_reviews_correct(self):
        print("NINETEENTH TEST")
        print("\n")

        print("BEFORE: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")

        self.review = self.env['monthly.review']
        self.review.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today() - relativedelta(months=1),
                    'customer_id': self.customers[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("AFTER A REVIEW: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")
        
        self.wrong_review = self.env['monthly.review']
        self.wrong_review.create([
                {
                    'new_weight': 90.0,
                    'new_height': 1.78,
                    'body_fat_percentage': 15,
                    'body_mass_index': 13,
                    'chest_measurement': 30,
                    'weist_measurement': 35,
                    'abdomen_measure': 30,
                    'hips_measure': 35,
                    'thighs_measure': 20,
                    'arms_measure': 15,
                    'date_made': datetime.date.today(),
                    'customer_id': self.customers[0].id
                }])

        print("AFTER: Number of reviews: " + str(len(self.customers[0].monthly_review_ids)))
        print("\n")

        var = self.assertEqual(2, len(self.customers[0].monthly_review_ids))
        return var

    
    #TESTS FOR TRAINING FUNCTIONALITY -----------------------------------------------------------------------


    def test_p_20_personal_training(self):
        print("TWENTYTH TEST")
        print("\n")

        print("BEFORE: Number of trainings: " + str(len(self.customers[0].customer_training_ids)))
        print("\n")

        self.training = self.env['customer.training']
        self.training.create([
                {
                    'name': "My training",
                    'numb_turns': 1,
                    'machine_use': True,
                    'training_machine_ids': self.machines[0],
                    'customer_id': self.customers[0].id
                }])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("AFTER: Number of trainings: " + str(len(self.customers[0].customer_training_ids)))
        print("\n")

        var = self.assertEqual(1, len(self.customers[0].customer_training_ids))
        return var


    def test_p_21_two_personal_trainings(self):
        print("TWENTY FIRST TEST")
        print("\n")

        print("BEFORE: Number of trainings: " + str(len(self.customers[0].customer_training_ids)))
        print("\n")

        self.training = self.env['customer.training']
        self.training.create([
                {
                    'name': "My training",
                    'numb_turns': 1,
                    'machine_use': True,
                    'training_machine_ids': self.machines[0],
                    'customer_id': self.customers[0].id
                },
                {
                    'name': "My training 2",
                    'numb_turns': 2,
                    'machine_use': True,
                    'training_machine_ids': [self.machines[0].id, self.machines[1].id],
                    'customer_id': self.customers[0].id
                }
                ])

        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("AFTER: Number of trainings: " + str(len(self.customers[0].customer_training_ids)))
        print("\n")

        var = self.assertEqual(2, len(self.customers[0].customer_training_ids))
        return var
    
    #TEST FOR EDITING DATA ---------------------------------------------------------------------------------------------------------------


    def test_p_22_edit_customer(self):
        print("TWENTY SECOND TEST")
        print("\n")
        #Solo el segundo está dado de baja ([1]), por lo tanto, el primero ([0]) está dado de alta.
        print("BEFORE:")
        print("Name: " + str(self.customers[0].name))
        print("Surnames: " + str(self.customers[0].surnames))
        print("Birth date: " + str(self.customers[0].birth_date))
        print("Age: " + str(self.customers[0].age))
        print("\n")

        self.socia_editada = self.customers[0].write({
            'name': 'Jose Maria',
            'surnames': 'Iglesias Bellido',
            'birth_date': datetime.date.today() - relativedelta(years=58)
        })
        
        print("AFTER:")
        print("Name: " + str(self.customers[0].name))
        print("Surnames: " + str(self.customers[0].surnames))
        print("Birth date: " + str(self.customers[0].birth_date))
        print("Age: " + str(self.customers[0].age))
        print("\n")
        var1 = self.assertEqual(self.customers[0].name, 'Jose Maria')
        var2 = self.assertEqual(self.customers[0].surnames, 'Iglesias Bellido')
        var3 = self.assertEqual(self.customers[0].birth_date, datetime.date.today() - relativedelta(years=58))
        var4 = self.assertEqual(self.customers[0].age, 58)
        res = var1 and (var2 and (var3 and (var4)))
        return res


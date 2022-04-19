from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install','estate')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstatePropertyTestCase, cls).setUpClass()
        print("\n")
        print("REALIZANDO SETUP DE TESTS DEL MODULO ESTATE")
        print("\n")

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'TestEstatePropertyExample', 
                'expected_price': 10000,
            },
            {
                'name': 'TestEstatePropertyExample2', 
                'expected_price': 20000,
            }
        ])
    
    #test para comprobar que se realiza la accion de poner a sold
    def test_action_sold_estate(self):
        print("\n")
        print("ANTES: " + str(self.properties[0].state) + " - " + str(self.properties[1].state))
        print("\n")
        self.properties.action_sold_estate()
        print("DESPUES: " + str(self.properties[0].state) + " - " + str(self.properties[1].state))
        print("\n")
        var = self.assertRecordValues(self.properties,[
            {'name': 'TestEstatePropertyExample', 'state': 'sold'},
            {'name': 'TestEstatePropertyExample2', 'state': 'sold'}
        ])
        '''with self.assertRaises(UserError):
            "ERROR A LA HORA DE HACER LA ACCION DE SOLD"'''
        return var
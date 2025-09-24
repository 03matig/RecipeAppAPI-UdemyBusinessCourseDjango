"""
Sample tests for the calc module
"""

from django.test import SimpleTestCase # We don't need any database integration for this particular test
from app import add, subtract

class CalcTests(SimpleTestCase):
    """ Test the calc module. """
    def test_add_numbers(self): # We add the self argument because it's a method
        """ Adding numbers together """

        res = add(5, 6)
        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """ Test subtracting numbers. """
        
        res = subtract(10,15)
        self.assertEqual(res, 5)
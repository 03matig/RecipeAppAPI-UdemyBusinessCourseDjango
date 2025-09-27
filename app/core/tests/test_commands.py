"""
Test custom Django management commands.
"""

from unittest.mock import patch

# OperationalError is an option of error we might get if we try to conect to the database before its ready.
from psycopg2 import OperationalError as Psycopg2Error  # psycopg2 in local will not be recognised, but it will inside the container

# django.core.management > local directory path for the management commands
# call command > helper function provided by Django that allows us to simmmulate (or to actually) calling the command that we're testing
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# We'll use SimpleTestCase as we'll be mocking in the functionality instead of lifting an actual database

# Mock the behavior of the database with patch:
@patch('core.management.commands.wait_for_db.Command.check')

class CommandTests(SimpleTestCase):
    """ Test commands. """

    def test_wait_for_db_ready(self, patched_check):
        """ Test waiting for database if database ready. """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # What should happen if the database isn't ready?
    """
    In unittest.mock, patched_check.side_effects lets defining: 
        A sequence of values/exceptions --> everytime you call the mock, 
            it returns the next value or throws
            the following exception.

        Or a function --> decides dinamically what happens
    
    In this case, a list of values/exceptions is what its used.
    """

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ 
        Database isn't ready so we wanna delay a few seconds and wait until 
        it's ready (get OperationalError).

        'The first two times we call the mocked method we want it to raise the Psycopg2Error. 
        The next three times we raise OperationalError. The last time it'll return the True boolean value'.

        Psycopg2Error means it's not ready to accept connections. 
        OperationalError means it's ready to accept connections but 
        it hasn't created the dev database we want to use. 
        
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + \
            [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

        patched_sleep(1)
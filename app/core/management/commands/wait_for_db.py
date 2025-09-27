# Name of this file is going to be the name of the command.
# Because of the structure of this directory, Django will automatically detect as a management command, that
# will then allow us to run it with "python manage.py"

"""
Django command to wait for the DataBase to be lifted and available
"""

# We import time so we can sleep the wait_for_db command between the connection requests
import time

# We import psycopg2.OperationalError as Psycopg2Error to diff between psycopg2 error and django.db.utils OperationalError
from psycopg2 import OperationalError as Psycopg2OpError  # Psycopg2Error is the error we get when db isn't ready to accept connections

from django.db.utils import OperationalError  # Django throws this errors when the db isn't lifted yet, but it accepts connections.
from django.core.management.base import BaseCommand

# Here, BaseCommand has a "check" method that verifies if the database is lifted and ready, allowing us
# to mock its behavior. This method is called by "directory.subdirectory.subsubdirectory.FileName.Class.check",
# or, in this case, "core.management.commands.wait_for_db.Command.check"


class Command(BaseCommand):
    """ Django command to wait for DataBase. """

    def handle(self, *args, **options):
        """ Entrypoint for command. """
        self.stdout.write("Waiting for database...") # stdout is the command we can use to log things to the screen as our command is executed. It's like logging.
        db_up = False # boolean default value
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except Psycopg2OpError as e:
                self.stdout.write(f'Psycopg2 error: {e}. Waiting 1 second...')
                time.sleep(1)

            except OperationalError as e:
                self.stdout.write(f'Django DB error: {e}. Waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
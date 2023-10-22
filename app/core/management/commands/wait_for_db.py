"""
Django command to wait for the database to  be available
"""
import time
from psycopg2 import OperationalError as Psycop2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycop2Error, OperationalError):
                self.stdout.write('Database Unavailable, waiting 1 second')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))

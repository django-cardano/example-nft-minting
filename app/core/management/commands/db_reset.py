import os
import re
from pathlib import Path

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

SUPERUSER_PASSWORD = '&jj;<#PX2+zyY_Z^'


class Command(BaseCommand):
    """
    The db_reset command can be used to reset the database to fresh, empty state
    """
    help = 'Resets the database.'

    def flush_database(self):
        db_info = settings.DATABASES['default']
        db_path = db_info['NAME']
        if os.path.exists(db_path):
            print("Flushing existing database")
            os.remove(db_path)

        Path(db_path).touch()


    def rebuild_initial_migrations(self):
        print("---------- REBUILDING INITIAL MIGRATION ----------")
        app_names = ('core',)

        migration_file_re = re.compile(r"^(\d+)_(.*)\.py$")

        for app_name in app_names:
            migration_path = os.path.join(settings.PROJECT_PATH, app_name, 'migrations')

            with os.scandir(migration_path) as entries:
                for entry in entries:
                    if migration_file_re.match(entry.name):
                        migration_file_path = os.path.join(migration_path, entry.name)
                        os.remove(migration_file_path)

        management.call_command('makemigrations')

    def initialize_database(self):
        print("Performing initial migration:")
        management.call_command('migrate')

    def seed_users(self):
        print("Initializing site:")

        print("---------- SEEDING DATABASE ----------")
        print("Creating superusers:")

        for admin_info in settings.ADMINS:
            User._default_manager.db_manager().create_superuser(**{
                User.USERNAME_FIELD: admin_info[0],
                User.EMAIL_FIELD: admin_info[1],
                'first_name': admin_info[0],
                'password': SUPERUSER_PASSWORD,
            })

    def handle(self, *args, **options):
        self.flush_database()
        self.rebuild_initial_migrations()
        self.initialize_database()
        self.seed_users()

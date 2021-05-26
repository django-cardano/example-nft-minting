import io
import os
import re

from pathlib import Path
from PIL import Image
from urllib import request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import management
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ...models import Asset

User = get_user_model()

ASSET_INFO_LIST = [{
    'name': 'Snowflake',
    'image': 'https://unsplash.com/photos/9yhy1FXlKwI/download?w=1920',
    'genre': 'Nature',
    'artist': 'Aaron Burden',
    'date_published': '2016-03-06',
}, {
    'name': 'Finding my Roots',
    'image': 'https://unsplash.com/photos/EwKXn5CapA4/download?w=1920',
    'genre': 'Nature',
    'location': 'California, USA',
    'artist': 'Jeremy Bishop',
    'date_published': '2018-02-12'

}, {
    'name': 'Wintergreen',
    'image': 'https://unsplash.com/photos/S9miGKjxmb4/download?w=1920',
    'genre': 'Nature',
    'location': 'Sorel, Canada',
    'artist': 'Alexandre Guimont',
    'twitter': '@guimz_visuals',
    'date_published': '2016-06-20',
}, {
    'name': 'Healthy Choices',
    'image': 'https://unsplash.com/photos/IGfIGP5ONV0/download?w=1920',
    'genre': 'Food',
    'artist': 'Anna Pelzer',
    'twitter': '@annapelzer',
    'date_published': '2017-12-06',
}, {
    'name': 'Breakfast of Champions',
    'image': 'https://unsplash.com/photos/Yn0l7uwBrpw/download?w=1920',
    'genre': 'Food',
    'artist': 'Jimmy Dean',
    'twitter': '@jimmydean',
    'date_published': '2020-11-30',
}, {
    'name': 'Colorblind',
    'image': 'https://unsplash.com/photos/M7Qzh_PD2mM/download?w=1920',
    'genre': 'Animals',
    'artist': 'Doruk Yemenici',
    'twitter': '@dorukyemenici',
    'date_published': '2019-02-25',
}, {
    'name': 'The Lone Ranger',
    'image': 'https://unsplash.com/photos/kfR-bCXblkw/download?w=1920',
    'genre': 'Animals',
    'artist': 'Deepak Nautiyal',
    'twitter': '@deepaknautiyal',
    'date_published': '2019-11-18',
}, {
    'name': 'Blue Handed',
    'image': 'https://unsplash.com/photos/KgRKlQXmHR0/download?w=1920',
    'genre': 'Animals',
    'artist': 'Hans-Jurgen Mager',
    'twitter': '@hansjurgen007',
    'date_published': '2020-05-29',
}, {
    'name': 'Powder Day',
    'image': 'https://unsplash.com/photos/8FG9tt8qZ-8/download?w=1920',
    'genre': 'Sports',
    'artist': 'Yann Allegre',
    'location': 'Les Menuires, France',
    'date_published': '2018-06-22',
}, {
    'name': 'Concrete Jungle',
    'image': 'https://unsplash.com/photos/a5cTQOYfuwc/download?w=1920',
    'genre': 'Architecture',
    'artist': 'Zac Wolff',
    'location': 'Bosco Verticale, Milan, Italy',
    'date_published': '2019-06-14',
}]


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

    def seed_users(self, superuser_password):
        print("Initializing site:")

        print("---------- SEEDING DATABASE ----------")
        print("Creating superusers:")

        for admin_info in settings.ADMINS:
            User._default_manager.db_manager().create_superuser(**{
                User.USERNAME_FIELD: admin_info[0],
                User.EMAIL_FIELD: admin_info[1],
                'first_name': admin_info[0],
                'password': superuser_password,
            })

    def seed_assets(self):
        print('--- GENERATING ASSETS ---')
        for asset_info in ASSET_INFO_LIST:
            asset_name = asset_info['name']
            image_url = asset_info['image']
            print('{}: {}'.format(asset_name, image_url))

            asset = Asset(name=asset_name, metadata=asset_info)
            with request.urlopen(image_url) as fp:
                image_bytes = fp.read()
                image = Image.open(io.BytesIO(image_bytes))

                asset_info.update({
                    'width': image.width,
                    'height': image.height,
                })

                image_type = image.format.lower()
                filename = '{}.{}'.format(slugify(asset_name), image_type)

                asset.image.save(
                    filename,
                    ContentFile(image_bytes),
                    save=False
                )

            asset.save()


    def add_arguments(self, parser):
        parser.add_argument('--password', type=str)

    def handle(self, *args, **options):
        self.flush_database()
        self.rebuild_initial_migrations()
        self.initialize_database()

        superuser_password = options.get('password', 'admin')
        self.seed_users(superuser_password)

        self.seed_assets()

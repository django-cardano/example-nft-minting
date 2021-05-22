from django.apps import AppConfig

APP_TITLE = 'Example NFT Minting'

class CoreConfig(AppConfig):
    name = 'app.core'
    verbose_name = 'Core'

    def ready(self):
        # Makes sure all signal handlers are connected
        # from app.core import handlers  # noqa
        from django.contrib import admin

        admin.site.site_title = APP_TITLE
        admin.site.site_header = APP_TITLE

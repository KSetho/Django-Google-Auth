from django.core.management.base import BaseCommand
from django.conf import settings
try:
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site
    ALLAUTH_AVAILABLE = True
except ImportError:
    ALLAUTH_AVAILABLE = False


class Command(BaseCommand):
    help = 'Setup Google OAuth application in Django admin'

    def handle(self, *args, **options):
        if not ALLAUTH_AVAILABLE:
            self.stdout.write(
                self.style.ERROR('django-allauth is not properly installed')
            )
            return

        try:
            # Get Google credentials from settings
            google_config = settings.SOCIALACCOUNT_PROVIDERS.get('google', {}).get('APP', {})
            client_id = google_config.get('client_id')
            secret = google_config.get('secret')

            if not client_id or not secret:
                self.stdout.write(
                    self.style.ERROR(
                        'Google client ID and secret not found in settings. '
                        'Please check your .env file and SOCIALACCOUNT_PROVIDERS setting.'
                    )
                )
                return

            # Get or create the default site
            site, created = Site.objects.get_or_create(
                pk=1,
                defaults={
                    'domain': 'localhost:8000',
                    'name': 'Development Site'
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created site: {site.domain}')
                )

            # Clean up any duplicate Google apps first
            google_apps = SocialApp.objects.filter(provider='google')
            if google_apps.count() > 1:
                self.stdout.write(
                    self.style.WARNING(f'Found {google_apps.count()} Google OAuth apps. Cleaning up duplicates...')
                )
                # Keep the first one, delete the rest
                apps_to_delete = google_apps[1:]
                for app in apps_to_delete:
                    app.delete()
                self.stdout.write(
                    self.style.SUCCESS('Removed duplicate Google OAuth apps')
                )

            # Check if Google app already exists
            try:
                social_app = SocialApp.objects.get(provider='google')
                social_app.client_id = client_id
                social_app.secret = secret
                social_app.name = 'Google OAuth'
                social_app.save()
                self.stdout.write(
                    self.style.SUCCESS('Updated existing Google OAuth app')
                )
            except SocialApp.DoesNotExist:
                # Create new Google app
                social_app = SocialApp.objects.create(
                    provider='google',
                    name='Google OAuth',
                    client_id=client_id,
                    secret=secret
                )
                self.stdout.write(
                    self.style.SUCCESS('Created new Google OAuth app')
                )
            except SocialApp.MultipleObjectsReturned:
                # This shouldn't happen after cleanup, but just in case
                self.stdout.write(
                    self.style.ERROR('Multiple Google OAuth apps found. Please clean up manually in Django admin.')
                )
                return

            # Associate with site
            social_app.sites.add(site)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Google OAuth app configured successfully!\n'
                    f'Provider: google\n'
                    f'Client ID: {client_id[:10]}...\n'
                    f'Site: {site.domain}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up Google OAuth: {str(e)}')
            )

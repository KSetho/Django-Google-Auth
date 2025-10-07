from django.core.management.base import BaseCommand
try:
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site
    ALLAUTH_AVAILABLE = True
except ImportError:
    ALLAUTH_AVAILABLE = False


class Command(BaseCommand):
    help = 'Clean up duplicate Google OAuth applications and check configuration'

    def handle(self, *args, **options):
        if not ALLAUTH_AVAILABLE:
            self.stdout.write(
                self.style.ERROR('django-allauth is not properly installed')
            )
            return

        try:
            # Check all Google apps
            google_apps = SocialApp.objects.filter(provider='google')
            
            self.stdout.write(f'Found {google_apps.count()} Google OAuth app(s):')
            
            for i, app in enumerate(google_apps):
                self.stdout.write(f'  {i+1}. ID: {app.id}, Name: "{app.name}", Client ID: {app.client_id[:10]}...')
                sites = app.sites.all()
                self.stdout.write(f'     Sites: {[site.domain for site in sites]}')
            
            if google_apps.count() > 1:
                self.stdout.write(
                    self.style.WARNING('Multiple Google OAuth apps found! This will cause errors.')
                )
                
                # Ask user if they want to clean up
                self.stdout.write('Keeping the first app and removing duplicates...')
                
                # Keep the first one, delete the rest
                first_app = google_apps.first()
                duplicates = google_apps[1:]
                
                for app in duplicates:
                    self.stdout.write(f'Deleting duplicate app: {app.name} (ID: {app.id})')
                    app.delete()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Cleaned up {len(duplicates)} duplicate(s). Kept app: {first_app.name} (ID: {first_app.id})')
                )
                
            elif google_apps.count() == 1:
                app = google_apps.first()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Single Google OAuth app found: {app.name} (ID: {app.id})')
                )
                
                # Check if it's associated with a site
                sites = app.sites.all()
                if not sites:
                    site = Site.objects.get(pk=1)
                    app.sites.add(site)
                    self.stdout.write(
                        self.style.SUCCESS(f'Associated app with site: {site.domain}')
                    )
                
            else:
                self.stdout.write(
                    self.style.WARNING('No Google OAuth apps found. Run: python manage.py setup_google_oauth')
                )
            
            # Check sites
            self.stdout.write('\nSite configuration:')
            sites = Site.objects.all()
            for site in sites:
                self.stdout.write(f'  Site ID {site.id}: {site.domain} - {site.name}')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error checking OAuth configuration: {str(e)}')
            )

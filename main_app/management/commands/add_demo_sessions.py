from django.core.management.base import BaseCommand
from datetime import datetime, date
from main_app.models import Session


class Command(BaseCommand):
    help = 'Add 10 demo sessions'

    def handle(self, *args, **options):
        current_year = datetime.now().year
        
        # Session demo data (academic years)
        sessions_data = [
            (2016, 2017),
            (2017, 2018),
            (2018, 2019),
            (2019, 2020),
            (2020, 2021),
            (2021, 2022),
            (2022, 2023),
            (2023, 2024),
            (2024, 2025),
            (2025, 2026),
        ]
        
        self.stdout.write(self.style.SUCCESS('Creating 10 demo sessions...'))
        
        created_count = 0
        for start_year, end_year in sessions_data:
            try:
                # Check if session already exists
                if Session.objects.filter(start_year=f"{start_year}-01-01", end_year=f"{end_year}-12-31").exists():
                    self.stdout.write(self.style.WARNING(f'Session {start_year}-{end_year} already exists, skipping...'))
                    continue
                
                # Create Session
                Session.objects.create(
                    start_year=date(start_year, 1, 1),
                    end_year=date(end_year, 12, 31)
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created session: {start_year}-{end_year}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating session {start_year}-{end_year}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count}/10 demo sessions!')
        )

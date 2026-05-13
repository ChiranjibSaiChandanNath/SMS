from django.core.management.base import BaseCommand
from main_app.models import Course


class Command(BaseCommand):
    help = 'Add 10 demo courses'

    def handle(self, *args, **options):
        # Course demo data
        courses_data = [
            "Computer Science",
            "Information Technology",
            "Electronics Engineering",
            "Mechanical Engineering",
            "Civil Engineering",
            "Business Administration",
            "Data Science",
            "Artificial Intelligence",
            "Software Engineering",
            "Web Development"
        ]
        
        self.stdout.write(self.style.SUCCESS('Creating 10 demo courses...'))
        
        created_count = 0
        for course_name in courses_data:
            # Check if course already exists
            if Course.objects.filter(name=course_name).exists():
                self.stdout.write(self.style.WARNING(f'Course "{course_name}" already exists, skipping...'))
                continue
            
            try:
                # Create Course
                Course.objects.create(name=course_name)
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created course: {course_name}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating {course_name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count}/10 demo courses!')
        )

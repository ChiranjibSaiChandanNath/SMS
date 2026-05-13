from django.core.management.base import BaseCommand
from main_app.models import Course, Staff, Subject


class Command(BaseCommand):
    help = 'Add 20 demo subjects (2 per course)'

    def handle(self, *args, **options):
        # Subject data mapped to courses
        subjects_by_course = {
            "Computer Science": ["Data Structures", "Database Management Systems"],
            "Information Technology": ["Network Security", "Web Technologies"],
            "Electronics Engineering": ["Digital Electronics", "Microprocessors"],
            "Mechanical Engineering": ["Thermodynamics", "Fluid Mechanics"],
            "Civil Engineering": ["Structural Analysis", "Geotechnical Engineering"],
            "Business Administration": ["Finance Management", "Human Resources"],
            "Data Science": ["Machine Learning", "Statistical Analysis"],
            "Artificial Intelligence": ["Neural Networks", "Natural Language Processing"],
            "Software Engineering": ["Software Design", "Project Management"],
            "Web Development": ["Frontend Development", "Backend Development"]
        }
        
        self.stdout.write(self.style.SUCCESS('Creating 20 demo subjects (2 per course)...'))
        
        created_count = 0
        
        # Get all staff members
        all_staff = list(Staff.objects.all())
        
        if not all_staff:
            self.stdout.write(self.style.ERROR('✗ No staff members found. Please create staff first!'))
            return
        
        staff_index = 0
        
        for course_name, subject_names in subjects_by_course.items():
            try:
                # Get the course
                course = Course.objects.get(name=course_name)
                
                for subject_name in subject_names:
                    # Check if subject already exists
                    if Subject.objects.filter(name=subject_name, course=course).exists():
                        self.stdout.write(self.style.WARNING(f'Subject "{subject_name}" in {course_name} already exists, skipping...'))
                        continue
                    
                    # Get the next staff member (cycle through staff)
                    staff = all_staff[staff_index % len(all_staff)]
                    staff_index += 1
                    
                    # Create Subject
                    Subject.objects.create(
                        name=subject_name,
                        staff=staff,
                        course=course
                    )
                    
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created subject: {subject_name} ({course_name}) - {staff.admin.first_name} {staff.admin.last_name}')
                    )
                    
            except Course.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'✗ Course "{course_name}" not found!'))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating subjects for {course_name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count}/20 demo subjects!')
        )

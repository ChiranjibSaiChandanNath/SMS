from django.core.management.base import BaseCommand
from main_app.models import Student


class Command(BaseCommand):
    help = 'Change student passwords to their respective first names'

    def handle(self, *args, **options):
        students = Student.objects.all()
        
        if not students:
            self.stdout.write(self.style.ERROR('✗ No students found!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Changing passwords for {students.count()} students...'))
        
        updated_count = 0
        
        for student in students:
            try:
                # Get the student's first name
                first_name = student.admin.first_name
                
                # Set password to first name
                student.admin.set_password(first_name)
                student.admin.save()
                
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Changed password for {student.admin.first_name} {student.admin.last_name} ({student.admin.email}) to: {first_name}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error updating password for {student.admin.first_name} {student.admin.last_name}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully updated {updated_count}/{students.count()} student passwords!')
        )

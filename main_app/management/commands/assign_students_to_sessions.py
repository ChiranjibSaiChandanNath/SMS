from django.core.management.base import BaseCommand
from main_app.models import Student, Session


class Command(BaseCommand):
    help = 'Assign students to sessions accordingly'

    def handle(self, *args, **options):
        students = Student.objects.all().order_by('id')
        sessions = Session.objects.all().order_by('id')
        
        if not students:
            self.stdout.write(self.style.ERROR('✗ No students found!'))
            return
        
        if not sessions:
            self.stdout.write(self.style.ERROR('✗ No sessions found!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Assigning {students.count()} students to {sessions.count()} sessions...'))
        
        updated_count = 0
        
        # Distribute students across sessions
        for index, student in enumerate(students):
            # Assign student to session based on index
            session = sessions[index % len(sessions)]
            
            if student.session != session:
                student.session = session
                student.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Assigned {student.admin.first_name} {student.admin.last_name} to session {session.start_year.year}-{session.end_year.year}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠ {student.admin.first_name} {student.admin.last_name} already in session {session.start_year.year}-{session.end_year.year}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully assigned/verified {updated_count} students to sessions!')
        )

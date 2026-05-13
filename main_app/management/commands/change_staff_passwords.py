from django.core.management.base import BaseCommand
from main_app.models import Staff


class Command(BaseCommand):
    help = 'Change staff/teacher passwords to their respective first names'

    def handle(self, *args, **options):
        staff = Staff.objects.all()
        
        if not staff:
            self.stdout.write(self.style.ERROR('✗ No staff members found!'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Changing passwords for {staff.count()} staff members...'))
        
        updated_count = 0
        
        for staff_member in staff:
            try:
                # Get the staff member's first name
                first_name = staff_member.admin.first_name
                
                # Set password to first name
                staff_member.admin.set_password(first_name)
                staff_member.admin.save()
                
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Changed password for {staff_member.admin.first_name} {staff_member.admin.last_name} ({staff_member.admin.email}) to: {first_name}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error updating password for {staff_member.admin.first_name} {staff_member.admin.last_name}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully updated {updated_count}/{staff.count()} staff passwords!')
        )

import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from main_app.models import CustomUser, Staff, Course, LeaveReportStaff, FeedbackStaff, Subject, Attendance, AttendanceReport


class Command(BaseCommand):
    help = 'Add 10 demo staff members with profile pictures'

    def generate_staff_image(self, staff_number, first_name, last_name):
        """Generate a demo profile picture with staff name"""
        # Create a new image with a random background color
        colors = [
            (52, 152, 219),   # Blue
            (46, 204, 113),   # Green
            (155, 89, 182),   # Purple
            (230, 126, 34),   # Orange
            (231, 76, 60),    # Red
            (41, 128, 185),   # Dark Blue
            (39, 174, 96),    # Dark Green
            (142, 68, 173),   # Dark Purple
            (214, 137, 20),   # Dark Orange
            (192, 57, 43),    # Dark Red
        ]
        
        bg_color = colors[staff_number % len(colors)]
        width, height = 300, 300
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font, fallback to default if not available
        try:
            font_large = ImageFont.truetype("arial.ttf", 60)
            font_small = ImageFont.truetype("arial.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw circle in center
        circle_center = width // 2
        circle_radius = 80
        draw.ellipse(
            [(circle_center - circle_radius, circle_center - circle_radius),
             (circle_center + circle_radius, circle_center + circle_radius)],
            fill=(255, 255, 255)
        )
        
        # Draw initials in circle
        initials = (first_name[0] + last_name[0]).upper()
        bbox = draw.textbbox((0, 0), initials, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = circle_center - text_width // 2
        text_y = circle_center - text_height // 2
        draw.text((text_x, text_y), initials, fill=bg_color, font=font_large)
        
        # Draw name below
        name_text = f"{first_name} {last_name}"
        bbox = draw.textbbox((0, 0), name_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, 200), name_text, fill=(255, 255, 255), font=font_small)
        
        # Save to BytesIO
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        return img_io

    def handle(self, *args, **options):
        # Delete old demo staff and all related records
        old_staff = Staff.objects.all()
        staff_ids = list(old_staff.values_list('id', flat=True))
        
        # Get subjects linked to staff first
        subjects = Subject.objects.filter(staff_id__in=staff_ids)
        subject_ids = list(subjects.values_list('id', flat=True))
        
        # Delete attendances linked to subjects
        Attendance.objects.filter(subject_id__in=subject_ids).delete()
        
        # Delete subjects linked to staff
        subjects.delete()
        
        # Delete related records
        LeaveReportStaff.objects.filter(staff_id__in=staff_ids).delete()
        FeedbackStaff.objects.filter(staff_id__in=staff_ids).delete()
        
        # Delete staff and their users
        old_staff.delete()
        
        # Get or create a course
        course, _ = Course.objects.get_or_create(name="Computer Science")
        
        # Staff demo data
        staff_data = [
            ("Rajesh", "Kumar", "M"),
            ("Priya", "Singh", "F"),
            ("Amit", "Patel", "M"),
            ("Neha", "Gupta", "F"),
            ("Vikram", "Sharma", "M"),
            ("Anjali", "Verma", "F"),
            ("Sanjay", "Mishra", "M"),
            ("Divya", "Rao", "F"),
            ("Arjun", "Nair", "M"),
            ("Isha", "Joshi", "F"),
        ]
        
        self.stdout.write(self.style.SUCCESS('Creating 10 demo staff members...'))
        
        created_count = 0
        for index, (first_name, last_name, gender) in enumerate(staff_data):
            email = f"{first_name.lower()}@{last_name.lower()}.com"
            password = f"password{index + 1}"
            
            # Check if staff already exists
            if CustomUser.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'Staff {email} already exists, skipping...'))
                continue
            
            try:
                # Generate demo profile picture
                img_io = self.generate_staff_image(index, first_name, last_name)
                
                # Create CustomUser
                custom_user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    address=f"{index + 1} Demo Street, Staff City, SC 12345",
                    user_type="2"  # Staff type
                )
                
                # Save profile picture
                custom_user.profile_pic.save(
                    f'staff_{index + 1}_profile.jpg',
                    ContentFile(img_io.read()),
                    save=True
                )
                
                # Create Staff record
                Staff.objects.create(
                    admin=custom_user,
                    course=course
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created staff: {first_name} {last_name} ({email})'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating {first_name} {last_name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count}/10 demo staff members!')
        )

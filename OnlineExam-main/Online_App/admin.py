from django.contrib import admin
from Online_App.models import User, Staff, Student
from datetime import datetime
from .models import User, Student, Staff, MainStaff 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'get_email', 'contact', 'subject', 'get_dob')

    def get_email(self, obj):
        return obj.user.email  # Fetch email from related User model

    def get_dob(self, obj):
        # Ensure dob is a date object and safely handle None values
        return obj.dob.strftime('%Y-%m-%d') if obj.dob and isinstance(obj.dob, datetime.date) else "No DOB"
    get_dob.short_description = 'Date of Birth'



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'guardian_name')
    search_fields = ('name', 'email', 'guardian_name')



# admin.py
from django.contrib import admin
from .models import TeacherPaperSettings

@admin.register(TeacherPaperSettings)
class TeacherPaperSettingsAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'school_name', 'logo_position', 'updated_at')
    list_filter = ('logo_position', 'created_at')
    search_fields = ('teacher__username', 'teacher__email', 'school_name')
    readonly_fields = ('created_at', 'updated_at')

from django.contrib import admin
from .models import Package


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'validity', 'is_active')
    list_filter = ('type', 'is_active')


admin.site.register(Package, PackageAdmin)
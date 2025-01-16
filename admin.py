from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from django import forms
from rangefilter.filters import DateRangeFilter

from import_export.admin import ExportActionModelAdmin
from import_export import resources

from .models import MasterTeacher, MasterSubject, Student, Attendance, BarcodeAttendanceData
from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin

# Register MasterTeacher model
class MasterTeacherResource(resources.ModelResource):
    class Meta:
        model = MasterTeacher

class MasterTeacherAdmin(admin.ModelAdmin, DjangoQLSearchMixin):
    resource_class = MasterTeacherResource
    list_display = ('id', 'name', 'email', 'is_admin', 'created_at', 'updated_at')
    search_fields = ('name', 'email')
    list_filter = ('is_admin',)
    ordering = ('-id',)

admin.site.register(MasterTeacher, MasterTeacherAdmin)

# Register MasterSubject model
class MasterSubjectAdmin(admin.ModelAdmin, DjangoQLSearchMixin):
    resource_class = MasterTeacherResource
    list_display = ('id', 'name', 'year', 'teacher')
    search_fields = ('name', 'teacher')
    list_filter = ('year', 'teacher')
    ordering = ('id',)

    # Display the number of students in the same course
    # def view_student_link(self, obj):
    #     student_count = obj.student_set.count()  # Ensure the related_name is correct if you have one
    #     url = reverse("admin:students_student_changelist") + "?" + urlencode({"subject__id": f"{obj.id}"})
    #     return format_html("<a href='{}'> {} Students </a>", url, student_count)

    # view_student_link.short_description = "No of students"

    # # Modify the teacher field label
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     form.base_fields['teacher'].label = "Teacher Name (CS teachers only!)"
    #     return form

admin.site.register(MasterSubject, MasterSubjectAdmin)

# Register Student model
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student

class StudentAdmin(ExportActionModelAdmin):
    resource_class = StudentResource
    list_display = ('id', 'roll_no', 'name', 'gender', 'email', 'phone', 'faculty', 'subject', 'academic_year')
    search_fields = ('name__startswith', 'email__startswith', 'roll_no', 'phone')
    list_filter = ('gender', 'faculty', 'subject', 'academic_year')
    # ordering = ('id',)
    list_per_page = 20

    # def show_avg(self, obj):
    #     from django.db.models import Sum
    #     result = Attendance.objects.filter(student=obj).aggregate(total_status=Sum('status'))  # Fixed issue here
    #     total_status = result['total_status']

    #     if total_status is not None:
    #         return format_html("<b><i>{}</i></b>", total_status)
    #     return "-"
    
    from django.db.models import Count

    # def show_avg(self, obj):
    #     # Count the number of 'present' statuses for the given student
    #     total_present = Attendance.objects.filter(student=obj, status='present').count()

    #     if total_present is not None:
    #         return format_html("<b><i>{}</i></b>", total_present)
    #     return "-"

    # show_avg.short_description = "AVG Attendance"


    # def show_sum(self, obj):
    #     # Count the number of 'present' statuses for the given student and subject
    #     total_present_for_subject = Attendance.objects.filter(student=obj, subject=obj.subject, status='present').count()
        
    #     if total_present_for_subject is not None:
    #         return format_html("<b><i>{}</i></b>", total_present_for_subject)
    #     return "-"
        
    # show_sum.short_description = "Subject Attendance"


admin.site.register(Student, StudentAdmin)

# Register Attendance model
class AttendanceResource(resources.ModelResource):
    class Meta:
        model = Attendance

class AttendanceAdmin(ExportActionModelAdmin):
    resource_class = AttendanceResource
    list_display = ('date', 'time','roll_no', 'student', 'subject', 'teacher', 'sessiontime', 'status')
    search_fields = ('student__name__startswith', 'subject__name__startswith', 'sessiontime', 'status')
    list_filter = ('date', 'sessiontime', 'status')
    ordering = ('-time',)
    list_per_page = 20

admin.site.register(Attendance, AttendanceAdmin)

# Register BarcodeAttendanceData model
class BarcodeAttendanceDataResource(resources.ModelResource):
    class Meta:
        model = BarcodeAttendanceData

class BarcodeAttendanceDataAdmin(admin.ModelAdmin, DjangoQLSearchMixin):
    list_display = ('id' ,'student' , 'barcode_data', 'time_scanned' , 'date_scanned')
    search_fields = ('student_name', 'id' , 'barcode_data')
    list_filter = ('date_scanned',)
    ordering = ('-time_scanned',)
    list_per_page = 20

admin.site.register(BarcodeAttendanceData, BarcodeAttendanceDataAdmin)

# Example: Register a Biometric Data Admin (commented out for now)
# class BiometricDataAdmin(admin.ModelAdmin, DjangoQLSearchMixin):
#     form = BiometricDataForm
#     list_display = ('id', 'date_created', 'student')
#     search_fields = ('std__name',)
#     list_filter = ('date_created',)
#     ordering = ('-date_created',)
#     list_per_page = 20
#     actions = ['capture_fingerprint_action']

#     def capture_fingerprint_action(self, request, queryset):
#         self.message_user(request, "Fingerprint capture initiated.")
#         return HttpResponseRedirect(request.get_full_path())

#     capture_fingerprint_action.short_description = "Capture Fingerprint"

#     class Media:
#         js = ('js/fingerprint_capture.js')

# admin.site.register(BarcodeAttendanceData, BiometricDataAdmin)

from django.shortcuts import render , redirect 
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from students.models import MasterTeacher , MasterSubject ,Student , BarcodeAttendanceData , Attendance
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator
from datetime import datetime 
import pandas as pd

# Logout view
def logout(request):
    auth_logout(request)
    request.session.flush()
    messages.success(request, 'You have logged out successfully!')
    return redirect('index')

@staff_member_required
def startattendance(request):
    
    if request.session.get('teacher') is not None:
        request.session.pop('teacher')
    if request.session.get('subject') is not None:
        request.session.pop('subject')
    if request.session.get('sessiontime') is not None:
        request.session.pop('sessiontime')
    if request.session.get('note') is not None:
        request.session.pop('note')
        
    # messages.success(request , "session cleared")
    
    if request.method == 'POST':
        teacher = request.POST.get('teacher')
        subject = request.POST.get('subject')
        sessiontime = request.POST.get('session')
        
        # if not teacher or not subject or not sessiontime:
        #     messages.error(request, 'Please fill all the fields')
        #     return redirect('startattendance')
        
         # here i need the logic that there is no teacher no record with same date with same teacher same sessiontime 
        
        existing_record = Attendance.objects.filter(
            date=datetime.today(),
            teacher__name=teacher,
            sessiontime=sessiontime
        ).exists()

        if existing_record:
            messages.error(request, 'Attendance for this teacher at the same session time already exists for today.')
            return redirect('startattendance')
        
        request.session['teacher'] = teacher
        request.session['subject'] = subject
        request.session['sessiontime'] = sessiontime

        messages.success(request, 'attendance started')
        return redirect('attendance')
        
    teachers = MasterTeacher.objects.all()
    subjects = MasterSubject.objects.all()
    return render(request, 'admin/biosystem/start.html', {'teachers':teachers , 'subjects' : subjects} )


@staff_member_required
def attendance(request):
    
    teacher = request.session.get('teacher') 
    subject = request.session.get('subject') 
    sessiontime = request.session.get('sessiontime') 
    
    if not teacher or not subject or not sessiontime :
        messages.error(request, 'there is no attendance data in session')
        return redirect('startattendance')

    try:
        teacher_instance = MasterTeacher.objects.get(name=teacher)
        subject_instance = MasterSubject.objects.get(name=subject)
    
    except MasterTeacher.DoesNotExist:
        messages.error(request, 'Teacher not found')
        return redirect('startattendance')
    
    except MasterSubject.DoesNotExist:
        messages.error(request, 'Subject not found')
        return redirect('startattendance')
    
    # i have input form for taking student barcode only 
    
    if request.method == 'POST':
        
        barcode_data = request.POST.get('barcode_data')
        
        if not barcode_data:
            messages.error(request, 'Please scan the barcode again')
            return redirect('attendance')
        
        try :
            std_with_same_barcode = BarcodeAttendanceData.objects.get(barcode_data = barcode_data)
        except BarcodeAttendanceData.DoesNotExist :
            
            messages.error(request, "there is no student with same Barcode")
            return redirect('attendance')
        
        student = std_with_same_barcode.student
        if not student :
            messages.error(request, "error to load the student object")
            return redirect('attendance')
    
    #    check that student is not in same session and and date with same teacher before i add his attendance
        
        existing_attendance = Attendance.objects.filter(
            date = datetime.today(),
            student=student,
            sessiontime=sessiontime,
            subject=subject_instance,
            teacher=teacher_instance,
            status='present'
        ).exists()

        if existing_attendance :
            messages.error(request, 'Attendance for this student in the same session and date with the same teacher already exists')
            return redirect('attendance')
        
        try :
            roll_no = std_with_same_barcode.student.roll_no
            attendance_record = Attendance.objects.create(sessiontime=sessiontime,  subject=subject_instance, teacher=teacher_instance,  status='present', roll_no=roll_no , student = student)
            attendance_record.save()
            messages.success(request, 'Attendance Marked Successfully')
        
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('attendance')
    
    return render(request , 'admin/biosystem/attendance.html')
    
    
@staff_member_required
def dashboard(request):
    # for latest attendance
    records = Attendance.objects.all().order_by('-time')
    # records = Attendance.objects.all()
    paginator = Paginator(records, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/biosystem/dashboard.html' , {'items':page_obj })

''' my logic '''
# @staff_member_required
# def end_attendance(request):
#     # before i denf the attendance i need to check that i have the data in session
#     teacher = request.session.get('teacher') 
#     subject = request.session.get('subject') 
#     sessiontime = request.session.get('sessiontime') 
    
#     if not teacher or not subject or not sessiontime :
#         messages.error(request, 'there is no attendance session to terminate')
#         return redirect('startattendance')
    
#     try:
#         teacher_instance = MasterTeacher.objects.get(name=teacher)
#         subject_instance = MasterSubject.objects.get(name=subject)
    
#     except MasterTeacher.DoesNotExist:
#         messages.error(request, 'can\'t create Instance of Teacher Object')
#         return redirect('startattendance')
    
#     except MasterSubject.DoesNotExist:
#         messages.error(request, 'can\'t create Instance of Subject Object')
#         return redirect('startattendance')
    
#     students = BarcodeAttendanceData.objects.all()
    
#     # add to filter student at same date time and session
    
    
#     for student in students:
        
#         attended_students = Attendance.objects.all().filter(
#             date = datetime.date.today(),
#             student=student,
#             sessiontime=sessiontime,
#             subject=subject_instance,
#             teacher=teacher_instance,
#             status='present'
#             ).exists()
        
#         if student not in attended_students :
            
#             try:
#                 student_instance = student.student
#                 std_roll_no = student_instance.roll_no
#                 if not student_instance :
#                     messages.error(request, 'Student not found')
#                     return redirect('admin:index')
                    
#                 absent_student = Attendance.objects.create(
#                     session=sessiontime,
#                     subject=subject_instance,
#                     teacher=teacher_instance,
#                     status='absent',
#                     roll_no = std_roll_no ,
#                     student=student_instance,
#                 )
#                 absent_student.save()
                 
#             except Exception as e:
#                 messages.error(request, f'Error: {e}')
#                 return redirect('admin:index')
    
#     messages.success(request, 'Absent students added Successfully')
#     # pop all the session data and redirect to admin:index
#     # request.session.pop('teacher')
#     # request.session.pop('subject') 
#     # request.session.pop('sessiontime')
#     # request.session.pop('note')
#     messages.success(request, 'Attendance Ended Successfully')
#     return redirect('admin:index')

'''chatgpt logic '''
@staff_member_required
def end_attendance(request):
    # Check that session data is available
    teacher = request.session.get('teacher') 
    subject = request.session.get('subject') 
    sessiontime = request.session.get('sessiontime') 
    
    if not teacher or not subject or not sessiontime:
        messages.error(request, 'Attendance session data is missing.')
        return redirect('startattendance')
    
    try:
        teacher_instance = MasterTeacher.objects.get(name=teacher)
        subject_instance = MasterSubject.objects.get(name=subject)
    except (MasterTeacher.DoesNotExist, MasterSubject.DoesNotExist) as e:
        messages.error(request, f'Error creating instance: {e}')
        return redirect('startattendance')
    
    # Filter students who have attended
    attended_students = Attendance.objects.filter(
        date=datetime.today(),
        sessiontime=sessiontime,
        subject=subject_instance,
        teacher=teacher_instance,
        status='present'
    ).values_list('student', flat=True)
    
    students = BarcodeAttendanceData.objects.exclude(student__in=attended_students)
    
    for student in students:
        try:
            student_instance = student.student
            if not student_instance:
                messages.error(request, 'Student not found')
                return redirect('admin:index')
                
            Attendance.objects.create(
                sessiontime=sessiontime,
                subject=subject_instance,
                teacher=teacher_instance,
                status='absent',
                roll_no=student_instance.roll_no,
                student=student_instance,
            )
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect('admin:index')
    
    
    # Clean up session data
    request.session.pop('teacher', None)
    request.session.pop('subject', None)
    request.session.pop('sessiontime', None)
    request.session.pop('note', None)
    
    messages.success(request, 'Absent students added Attendance ended successfully')
    return redirect('admin:index')


@staff_member_required
def add_student(request):
    if request.method == 'POST':
        
        student_name = request.POST.get('student_name')
        barcode_data = request.POST.get('barcode_data')
        
        if student_name and barcode_data :
            try:
                student = Student.objects.get(name=student_name)
                # std_Roll_number = Student.objects.get(name=student_name).roll_no
                if not BarcodeAttendanceData.objects.filter(student=student).exists():
                    student_data = BarcodeAttendanceData.objects.create(student=student, barcode_data=barcode_data)
                    student_data.save()
                    messages.success(request, 'Student Added Successfully')
                else:
                    messages.error(request, "Student with the same name is already in the Barcode table")
                    return redirect('add_student')
                
            except Student.DoesNotExist:
                messages.error(request, 'Student not found')
                return redirect('add_student')
        else:
            messages.error(request, 'Please fill all the fields')
            return redirect('add_student')
            
        return redirect('add_student')
            
    students = Student.objects.all()
    return render(request, 'admin/biosystem/addstudent.html', {'students':students})


@staff_member_required
def report(request):
    # Query to get the attendance data with the necessary fields
    attendance_data = Attendance.objects.values(
        'student__roll_no', 'student__name', 'date', 'teacher__name', 'sessiontime', 'status'
    )

    # Convert data to pandas DataFrame
    df = pd.DataFrame(attendance_data)

    # Create a new column combining date, teacher name, and session time as the column header
    df['date_teacher_session'] = df['date'].astype(str) + ' | ' + df['teacher__name'] + ' | ' + df['sessiontime']

    # Pivot the data - use student roll no as index, and date_teacher_session as columns
    pivot_df = df.pivot_table(
        index='student__roll_no',
        columns='date_teacher_session',
        values='status',
        aggfunc=lambda x: x.max(),  # We assume max works here since the status can only be 'present' or 'absent'
        fill_value='absent'  # Default to 'absent' if no data
    )

    # Convert the pivoted DataFrame to a list of dictionaries for easy rendering in HTML
    pivoted_attendance = pivot_df.reset_index().to_dict(orient='records')

    # Prepare column headers as a list (excluding the roll number column)
    column_headers = pivot_df.columns.tolist()

    # Count present and absent times for each student
    for student in pivoted_attendance:
        present_count = 0
        absent_count = 0
        # Loop through each column (attendance record for each session) for a student
        for col in column_headers:
            if student.get(col) == 'present':
                present_count += 1
            elif student.get(col) == 'absent':
                absent_count += 1
        # Add the counts to the student dictionary
        student['present_count'] = present_count
        student['absent_count'] = absent_count

    # Pass the pivoted data and column headers to the template
    return render(request, 'report.html', {
        'attendance_data': pivoted_attendance,
        'columns': column_headers,
    })



@staff_member_required
def report_dashboard(request):
    # Query to get the attendance data with the necessary fields
    attendance_data = Attendance.objects.values(
        'student__roll_no', 'student__name', 'date', 'teacher__name', 'sessiontime', 'status'
    )

    # Convert data to pandas DataFrame
    df = pd.DataFrame(attendance_data)

    # Create a new column combining date, teacher name, and session time as the column header
    df['date_teacher_session'] = df['date'].astype(str) + ' | ' + df['teacher__name'] + ' | ' + df['sessiontime']

    # Pivot the data - use student roll no as index, and date_teacher_session as columns
    pivot_df = df.pivot_table(
        index='student__roll_no',
        columns='date_teacher_session',
        values='status',
        aggfunc=lambda x: x.max(),  # We assume max works here since the status can only be 'present' or 'absent'
        fill_value='absent'  # Default to 'absent' if no data
    )

    # Convert the pivoted DataFrame to a list of dictionaries for easy rendering in HTML
    pivoted_attendance = pivot_df.reset_index().to_dict(orient='records')

    # Prepare column headers as a list (excluding the roll number column)
    column_headers = pivot_df.columns.tolist()

    # Count present and absent times for each student
    for student in pivoted_attendance:
        present_count = 0
        absent_count = 0
        # Loop through each column (attendance record for each session) for a student
        for col in column_headers:
            if student.get(col) == 'present':
                present_count += 1
            elif student.get(col) == 'absent':
                absent_count += 1
        # Add the counts to the student dictionary
        student['present_count'] = present_count
        student['absent_count'] = absent_count

    # Pass the pivoted data and column headers to the template
    return render(request, 'admin/biosystem/report.html', {
        'attendance_data': pivoted_attendance,
        'columns': column_headers,
    })


    


@staff_member_required
def my_admin_view4(request):
    return HttpResponse('This is my custom admin page 4.')

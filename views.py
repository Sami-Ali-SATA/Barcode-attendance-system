from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.hashers import check_password, make_password
from functools import wraps
from .models import Student
from django.core.files.storage import FileSystemStorage

from django.contrib import admin

# Decorator to check if the user is a student
def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student:
            return HttpResponseForbidden("You must be a student to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# View to serve student image
def student_image(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    image_data = open(student.image.path, "rb").read()
    return HttpResponse(image_data, content_type="image/jpeg")

# Admin page
def admin_page(request):
    return admin.site.login(request)
    
# Home view
def index(request):
    return render(request, 'index.html')

# About us view
def about(request):
    return render(request, 'about_us.html')

# Developer view
def developer_profile(request):
    return render(request, 'dev.html')

# Guide view
def guide(request):
    return render(request, 'guide.html')

# Test view
def test(request):
    return render(request, 'test.html')

# pagenotfount
def pagenotfount(request):
    return render(request, 'pagenotfount.html')

def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_page_not_found


# Student login view
def login(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('profile', student_id=request.user.id)
    
    if request.user.is_superuser:
        return redirect('admin:index')
    
    if request.method == 'POST' :
    
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password :
            messages.error(request, "please fill all the fields")
            print("please fill all the fields")
            return redirect('login')
            
        user = Student.objects.filter(email=email).first()

        if user :
            if check_password(password, user.password):
            
                auth_login(request, user)
                messages.success(request, f'User {email} logged in successfully')
                print(f'User {email} logged in successfully')
                return redirect('profile', student_id=user.id)
            
            else:
                messages.error(request, 'Incorrect password.')
                print("Incorrect password.")
                return redirect('login')
        else :
            messages.error(request, "Incorrect User ! ") 
            print("Incorrect User ! ")
            return redirect('login')
            
    return render(request, 'registration/login.html', {'messages': messages.get_messages(request)})


# Logout view
def logout(request):
    auth_logout(request)
    request.session.flush()
    messages.success(request, 'You have logged out successfully!')
    return redirect('index')

# Registration view
def register(request):
    if request.user.is_authenticated:
        return redirect('profile', student_id=request.user.id)

    if request.method == 'POST':
        std_roll = request.POST.get('std_Roll')
        std_name = request.POST.get('std_name')
        std_gender = request.POST.get('std_gender')
        std_dob = request.POST.get('std_dob')
        std_blood_group = request.POST.get('std_blood_group')
        std_email = request.POST.get('std_email')
        std_phone = request.POST.get('std_phone')
        std_addr = request.POST.get('std_addr')
        std_faculty = request.POST.get('std_faculty')
        std_subject = request.POST.get('std_subject')
        std_acd_year = request.POST.get('std_acd_year')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        std_image = request.FILES.get('std_image')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if Student.objects.filter(email=std_email).exists():
            messages.error(request, 'User with the same Email already exists!')
            return redirect('register')

        if not std_image:
            messages.error(request, 'Profile image is required!')
            return redirect('register')

        student = Student(
            roll_no=std_roll,
            name=std_name,
            gender=std_gender,
            dob=std_dob,
            blood_group=std_blood_group,
            email=std_email,
            phone=std_phone,
            address=std_addr,
            faculty=std_faculty,
            subject=std_subject,
            academic_year=std_acd_year,
            image=std_image,
            password=make_password(password)
        )
        student.save()
        auth_login(request, student)

        messages.success(request, 'Successful Registration!')
        auth_login(request, student)
        
        return redirect('profile', student_id=student.id)
    
    else:
        return render(request, 'register.html')


# Student profile view
@login_required
def profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.user.is_superuser:
        messages.error(request, "Admin has no permission to view student profiles.")
        return redirect("index")

    if student.id != request.user.id:
        messages.error(request, "You do not have permission to view this profile.")
        return redirect('index')

    return render(request, 'registration/std_profile.html', {'student': student})


# Update login password view
@login_required
def login_pass_update(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldpass')
        new_password = request.POST.get('newpass')
        confirm_new_password = request.POST.get('conf_newpass')

        if not old_password or not new_password or not confirm_new_password:
            messages.warning(request, "Please fill out all fields.")
            return redirect('profile', student_id=request.user.id)

        if old_password == new_password:
            messages.error(request, "The new password cannot be the same as the old password.")
            return redirect('profile', student_id=request.user.id)

        if new_password != confirm_new_password:
            messages.error(request, "The new passwords do not match.")
            return redirect('profile', student_id=request.user.id)

        if not check_password(old_password, request.user.password):
            messages.error(request, "The old password you entered is incorrect.")
            return redirect('profile', student_id=request.user.id)

        request.user.password = make_password(new_password)
        request.user.save()
        messages.success(request, 'Password has been updated, please log in again.')
        return redirect('login')

    return redirect('profile', student_id=request.user.id)


# Update password (forgotten password)
def update_password(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if not email or not phone:
            messages.error(request, "Email and Phone Number fields can't be empty")
            return redirect('update_password')
        
        user = Student.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No such user exists")
            return redirect('update_password')

        if phone != user.phone:
            messages.error(request, "There is no user with the same phone number")
            return redirect('update_password')

        request.session['cemail'] = email
        return redirect('up_ppass')
    else:
        return render(request, 'update_password.html')


# Reset password view
def up_ppass(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        uemail = request.session.get('cemail')
        new_pass = request.POST.get('newpass')
        conf_newpass = request.POST.get('conf_newpass')

        if not uemail:
            messages.error(request, "Email does not exist in session, please try again")
            return redirect('update_password')

        if not new_pass or not conf_newpass:
            messages.error(request, "Make sure you inserted some data")
            return redirect('up_ppass')

        if new_pass != conf_newpass:
            messages.error(request, "Passwords do not match")
            return redirect('up_ppass')
        
        user = Student.objects.filter(email=uemail).first()
        if user:
            user.password = make_password(new_pass)
            user.save()
            request.session.pop('cemail')
            messages.success(request, "Password updated successfully")
            return redirect('login')
        else:
            messages.error(request, "User does not exist to update their password")

    return render(request, 'up_ppass.html')


# Update student bio
@login_required
def std_update_bio(request):
    if request.method == 'POST':
        fname = request.POST.get('f_name')
        lname = request.POST.get('l_name')
        city = request.POST.get('city')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        if not fname or not lname or not city or not phone or not password:
            messages.error(request, "Please fill all fields; no empty data required")
            return redirect('profile', student_id=request.user.id)

        if not check_password(password, request.user.password):
            messages.error(request, "Wrong password")
            return redirect('profile', student_id=request.user.id)

        request.user.name = f"{fname.capitalize()} {lname.capitalize()}"
        request.user.phone = phone
        request.user.address = city.capitalize()
        request.user.save()
        messages.success(request, "Your bio data has been updated. Change only when necessary")
        return redirect('profile', student_id=request.user.id)

    return redirect('profile', student_id=request.user.id)


# Update student photo
@login_required
def update_std_photo(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        file = request.FILES.get('image')

        if not file:
            messages.error(request, "Please upload photo and confirm your password")
            return redirect('profile', student_id=request.user.id)

        if not password:
            messages.error(request, "Please confirm your password")
            return redirect('profile', student_id=request.user.id)

        if not check_password(password, request.user.password):
            messages.error(request, "Wrong password")
            return redirect('profile', student_id=request.user.id)

        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        request.user.image = file_url
        request.user.save()
        messages.success(request, "Profile image updated")
        return redirect('profile', student_id=request.user.id)

    return redirect('profile', student_id=request.user.id)





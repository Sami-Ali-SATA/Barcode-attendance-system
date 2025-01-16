# app/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from django import forms
from django.core.exceptions import ValidationError
from .models import Student  # Import your Student model here

# for gingerprint decive
from django import forms



YEAR_CHOICES = [(str(year), str(year)) for year in range(2020, 2026)]

faculty_choices = {
    'BA': ['Marathi', 'Hindi', 'English', 'Geography', 'Political Science', 'Sociology', 'History', 'Home Science'],
    'BCom': ['Economics', 'English', 'Financial Accounting', 'Insurance', 'Principles of Marketing', 'Principles of Business Management'],
    'BSc': ['Physics', 'Chemistry', 'Mathematics', 'Statistics', 'Electronics', 'Computer Science', 'Botany', 'Zoology', 'Microbiology', 'Biotechnology', 'English'],
    'BCS': ['Mathematics', 'Electronics', 'Statistics', 'Computer Science', 'English'],
    'Biotech': ['Biotech-Entire'],
    'BBA': ['BBA'],
    'BCA': ['BCA'],
    'BVoc': ['B.Voc. Animation', 'B.Voc. Graphic Design', 'Photography']
}

class RegistrationForm(forms.Form):
    std_dob = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}) ,required=True )
    std_Roll = forms.CharField(label='Roll Number', required=True )
    std_name = forms.CharField(label='Name', required=True)
    std_gender = forms.ChoiceField(label='Gender', choices=[('Male', 'Male'), ('Female', 'Female')], required=True)
    std_blood_group = forms.ChoiceField(label=" choose your blood group", choices=[('A+', 'A+'),('A-', 'A-'),('B+', 'B+'),('B-', 'B-'),('AB+', 'AB+'),('AB-', 'AB-'),('O+', 'O+'),('O-', 'O-')], required=True)
    std_email = forms.EmailField(label='Email' , required=True)
    std_phone = forms.CharField(label='Phone', required=True )
    std_addr = forms.CharField(label='Address', widget=forms.Textarea , required=True)
    std_faculty = forms.ChoiceField(label='Faculty', choices=[('B.A', 'B.A'),('B.Com', 'B.Com'),('B.Sc', 'B.Sc'),('B.CS', 'B.Sc CS Entire'),('Biotech', 'B.Sc. Biotech'),('BBA', 'BBA'),('BCA', 'BCA'),('B.Voc', 'B.Voc')], required=True)
    std_subject = forms.ChoiceField(label='Choose Subject', required=True , choices=[
        ('B.Voc. Animation', 'B.Voc. Animation'),
        ('B.Voc. Graphic Design', 'B.Voc. Graphic Design'),
        ('BBA', 'BBA'),
        ('Biotech-Entire', 'Biotech-Entire'),
        ('Biotechnology', 'Biotechnology'),
        ('Botany', 'Botany'),
        ('BCA', 'BCA'),
        ('Chemistry', 'Chemistry'),
        ('Computer Science', 'Computer Science'),
        ('Economics', 'Economics'),
        ('Electronics', 'Electronics'),
        ('English', 'English'),
        ('Financial Accounting', 'Financial Accounting'),
        ('Geography', 'Geography'),
        ('History', 'History'),
        ('Home Science', 'Home Science'),
        ('Hindi', 'Hindi'),
        ('Insurance', 'Insurance'),
        ('Mathematics', 'Mathematics'),
        ('Microbiology', 'Microbiology'),
        ('Physics', 'Physics'),
        ('Photography', 'Photography'),
        ('Principles of Business Management', 'Principles of Business Management'),
        ('Principles of Marketing', 'Principles of Marketing'),
        ('Political Science', 'Political Science'),
        ('Sociology', 'Sociology'),
        ('Statistics', 'Statistics'),
        ('Zoology', 'Zoology')
            ]
        )

    
    std_acd_year = forms.ChoiceField(label=" Academic Year", required=True , choices=[('first year','first year'),('second year','second year'),('third year','third year'),('fourth year','fourth year')])
    std_p_addr = forms.CharField(label='Permanent Address', widget=forms.Textarea ,required=True)
    std_p_contact = forms.CharField(label='Permanent Contact', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput , required=True)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput , required=True)
    std_image = forms.ImageField(label='Profile Image', required=True)

    
    class Meta:
        model = Student
        fields = ['std_roll', 'std_name', 'std_gender', 'std_dob', 'std_blood_group', 'std_email', 'std_phone',
                  'std_addr', 'std_faculty', 'std_subject', 'std_acd_year', 'std_p_addr', 'std_p_contact',
                  'std_image', 'password', 'confirm_password']

    def clean_std_image(self):
        image = self.cleaned_data.get('std_image')
        if image:
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError('Invalid image format. Please upload a PNG, JPG, or JPEG file.')
        return image

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Passwords do not match!')


#### 2. Login Form

class LoginForm(forms.Form):
    email = forms.EmailField(label='Your Email' , widget= forms.EmailInput , required= True )
    password = forms.CharField(label='Your Password', widget=forms.PasswordInput , required= True)

#### 3. Admin Login Form

class AdminLoginForm(forms.Form):
    user_email = forms.EmailField(label='Your Email')
    user_password = forms.CharField(label='Your Password', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Remember Me', required=False)

#### 4. Admin Password Reset Form

class AdminPassForm(forms.Form):
    oldpass = forms.CharField(widget=forms.PasswordInput())
    newpass = forms.CharField(widget=forms.PasswordInput())
    conf_newpass = forms.CharField(widget=forms.PasswordInput())


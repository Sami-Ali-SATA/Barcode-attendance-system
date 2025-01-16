from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=150, null=False)
    password = models.CharField(max_length=150, null=False)
    last_login = models.DateTimeField(auto_now=True)
    is_student = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email', 'password']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
        ordering = ['-created_at']

# MasterTeachers are controled in admin page only
class MasterTeacher(models.Model):
    name = models.CharField(max_length=25, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=25, null=False)
    is_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Master Teacher'
        verbose_name_plural = 'Master Teachers'
        db_table = 'master_teacher'
        ordering = ['-created_at']

# MasterSubjects are controled in admin page only
class MasterSubject(models.Model):
    FIRST_YEAR = "First Year"
    SECOND_YEAR = "Second Year"
    THIRD_YEAR = "Third Year"
    
    CLASS_CHOICES = [
        (FIRST_YEAR, "First Year"),
        (SECOND_YEAR, "Second Year"),
        (THIRD_YEAR, "Third Year"),
    ]
    
    name = models.CharField(max_length=30, null=False)
    year = models.CharField(max_length=30, choices=CLASS_CHOICES, null=False, default=THIRD_YEAR)
    teacher = models.ForeignKey(MasterTeacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Master Subject'
        verbose_name_plural = 'Master Subjects'
        db_table = 'master_subject'
        ordering = ['name']

# stduents model for storing student data
class Student(models.Model):
    roll_no = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    gender = models.CharField(max_length=10, null=False)
    dob = models.DateField(null=False)
    blood_group = models.CharField(max_length=5, null=False)
    email = models.EmailField(unique=True, null=False)
    phone = models.DecimalField(max_digits=10 , decimal_places=0 , null=False)
    address = models.CharField(max_length=200, null=False)
    faculty = models.CharField(max_length=50, null=False)
    subject = models.CharField(max_length=50, null=False)
    academic_year = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to='student_images/', null=False)
    password = models.CharField(max_length=100, null=False)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email', 'password']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        db_table = 'students'
        ordering = ['-created_at', 'roll_no']

class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='studentprofile')

@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(student=instance)

@receiver(post_save, sender=Student)
def save_student_profile(sender, instance, **kwargs):
    instance.studentprofile.save()


# barcode attendance data model
class BarcodeAttendanceData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE )
    # barcode_data = models.DecimalField(max_digits=10 , decimal_places=0 , null=False )
    barcode_data = models.CharField(max_length=20, null=False)
    # scanned_at = models.DateTimeField(default=timezone.now)
    date_scanned = models.DateField(auto_now_add=True)
    time_scanned = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Student(id={self.id}, name={self.student.name}, scanned_at={self.date_scanned})"
    
    class Meta:
        verbose_name = 'Barcode Data'
        verbose_name_plural = 'Barcode Data Records'
        db_table = 'barcode_data'
        ordering = ['-time_scanned']

# attendance records model
class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sessiontime = models.CharField(max_length=20, null=False)
    subject = models.ForeignKey(MasterSubject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(MasterTeacher, on_delete=models.CASCADE, null=True)
    
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')], default='absent')
    roll_no = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.date} : {self.student} - {self.sessiontime}'

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        db_table = 'attendance'
        ordering = ['-date', '-time']

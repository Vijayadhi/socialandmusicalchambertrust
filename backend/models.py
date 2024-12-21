import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from backend.managers import CustomUserManager


# Function to generate random registration numbers
def generate_teacher_reg_num():
    return f"T-{uuid.uuid4().hex[:8].upper()}"


def generate_student_reg_num():
    return f"ST-{uuid.uuid4().hex[:8].upper()}"


def generate_tsreg_num():
    return f"TSREG-{uuid.uuid4().hex[:8].upper()}"


# CustomUser Model (Base model for common fields)
class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=120, unique=False, null=True, blank=True)
    name = models.CharField(max_length=35)
    email = models.EmailField(unique=True)
    reg_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, unique=True)
    alternate_number = models.CharField(max_length=10, null=True, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    ROLE_CHOICES = (
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )

    role = models.CharField(max_length=7, choices=ROLE_CHOICES)


    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'mobile_number']


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'custom_user'



# Student Model (One-to-One relationship with CustomUser)
class Student(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_profile')

    reg_num = models.CharField(max_length=20, unique=True, default=generate_student_reg_num)
    dob = models.DateField()
    grade_studying = models.CharField(max_length=50)
    father_name = models.CharField(max_length=35)
    mother_name = models.CharField(max_length=35)
    name_of_guru = models.CharField(max_length=255, null=True, blank=True)
    guru_mobile_number = models.CharField(max_length=10, null=True, blank=True)
    guru_registration_number = models.CharField(max_length=20, null=True, blank=True)
    name_of_institute = models.CharField(max_length=255, null=True, blank=True)
    address_of_institute = models.TextField(null=True, blank=True)
    payment_ref_no = models.CharField(max_length=100, unique=True)
    payment_proof = models.URLField(unique=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} ({self.reg_num})"

    class Meta:
        db_table = 'student'

    # Override save method to add logic for GuruStudentAssociation
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the student object first

        if self.guru_registration_number:
            try:
                guru = Guru.objects.get(reg_num=self.guru_registration_number)
                association, created = GuruStudentAssociation.objects.get_or_create(guru=guru)

                # Add this student to the association if not already present
                if not association.students.filter(id=self.id).exists():
                    association.students.add(self)

            except Guru.DoesNotExist:
                # Log or handle the absence of the Guru if needed
                pass


# Teacher Model (Separate model for teacher-specific details)
class Guru(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    reg_num = models.CharField(max_length=20, unique=True, default=generate_teacher_reg_num)
    name_of_institute = models.CharField(max_length=255)
    address_of_institute = models.TextField()
    profile_photo = models.URLField()
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} ({self.reg_num})"

    class Meta:
        db_table = 'guru'


# Association Model for Guru and Student
class GuruStudentAssociation(models.Model):
    id = models.BigAutoField(primary_key=True)
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name="students")

    class Meta:
        db_table = "guru_student_association"


# Batch Model (for multiple students registration)
# class Batch(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     guru = models.ForeignKey(Guru, on_delete=models.CASCADE, related_name='batches')
#     created_at = models.DateTimeField(auto_now_add=True)
#     students = models.ManyToManyField(Student, related_name="student")
#     def __str__(self):
#         return f"Batch by {self.guru.user.name}"
#
#     class Meta:
#         db_table = "batch"


# TeacherStudentRegistration Model (Many-to-one relationship between teacher and student)
# class TeacherStudentRegistration(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     reg_num = models.CharField(max_length=20, unique=True, default=generate_tsreg_num)
#     guru = models.ForeignKey(Guru, on_delete=models.CASCADE, related_name='teacher_students')
#     batch = models.ManyToManyField(Batch, related_name='teacher_batch')
#
#     def __str__(self):
#         return f"{self.guru.user.username} - {self.student.user.username}"

    # def save(self, *args, **kwargs):
    #     # Ensure that the student is registered by the correct teacher
    #     if self.student.user.teacher_profile != self.guru:
    #         raise ValueError(f"The student {self.student.user.username} is not registered by this teacher.")
    #     super().save(*args, **kwargs)

    # class Meta:
    #     db_table = "teacher_student_registration"
    #     unique_together = ('teacher', 'student')

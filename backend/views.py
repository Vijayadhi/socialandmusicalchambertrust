from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Guru, Student, GuruStudentAssociation, BulkStudentRegistration

# Create your views here.
# def registerGuru(request):
#     if(request.method == "POST"):
#
#     return render(request, "backend/guruRegistration.html")

# def studentRegistration(request):
#     return render(request, "backend/studentRegistration.html")


from django.shortcuts import render
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Guru


def registerGuru(request):
    context = {}

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Extract fields from POST and FILES
                name = request.POST.get('name')
                email = request.POST.get('email')
                mobile_number = request.POST.get('mobile_number')
                profile_photo = request.FILES.get('profile')  # FILE upload
                # password = request.POST.get('password')
                # confirm_password = request.POST.get('confirm_password')
                name_of_institute = request.POST.get('name_of_institute')
                address_of_institute = request.POST.get('address_of_institute')

                print([name, email, mobile_number, profile_photo,name_of_institute, address_of_institute])

                # Retain form data for repopulation in case of errors
                context['form_data'] = {
                    'name': name,
                    'email': email,
                    'mobile_number': mobile_number,
                    'name_of_institute': name_of_institute,
                    'institution_address': address_of_institute,
                }

                # Validate required fields
                if not all([name, email, mobile_number, profile_photo,name_of_institute, address_of_institute]):
                    messages.error(request, "All fields are required.")
                    return render(request, 'backend/guruRegistration.html', context)

                # Validate password confirmation
                # if password != confirm_password:
                #     messages.error(request, "Passwords do not match.")
                #     return render(request, 'backend/guruRegistration.html', context)

                # Create CustomUser
                user = CustomUser.objects.create(
                    name=name,
                    email=email,
                    mobile_number=mobile_number,
                    password=make_password("GurU2025"),
                    role='TEACHER'
                )

                # Add User to Group
                try:
                    guru_group, created = Group.objects.get_or_create(name='Guru')
                    user.groups.add(guru_group)
                except Exception as e:
                    raise ValidationError("Failed to add user to 'Guru' group.")

                # Create Guru Instance
                guru = Guru.objects.create(
                    user=user,
                    name_of_institute=name_of_institute,
                    address_of_institute=address_of_institute,
                    profile_photo=profile_photo
                )

                # Success Message
                messages.success(request, f"Registration successful! Your registration number is {guru.reg_num}.")
                return render(request, "backend/guruRegistration.html", context)

        except ValidationError as ve:
            messages.error(request, f"Validation Error: {str(ve)}")
        except Exception as e:
            print(e)
            messages.error(request, f"Registration failed: {str(e)}")

    return render(request, "backend/guruRegistration.html", context)

def studentRegistration(request):
    context = {}

    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        father_name = request.POST.get('father_name')
        guru_name = request.POST.get('guru_name')
        guru_mobile_number = request.POST.get('guru_mobile_number')
        guru_reg_num = request.POST.get('guru_reg_num')
        name_of_institute = request.POST.get('name_of_institute')  # Fixed typo
        payment_ref_number = request.POST.get('payment_ref_number')
        payment_proof = request.FILES.get('payment_proof')  # File upload

        try:
            # Validation checks
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError("Email already registered.")

            if CustomUser.objects.filter(mobile_number=mobile_number).exists():
                raise ValidationError("Mobile number already registered.")

            if Student.objects.filter(payment_ref_no=payment_ref_number).exists():
                raise ValidationError("Payment reference number already used.")

            # Create the CustomUser (student user)
            user = CustomUser.objects.create(
                name=name,
                email=email,
                mobile_number=mobile_number,
                password=make_password("StudenT2025"),  # Default password
                role='STUDENT',
            )

            # Add user to 'Student' group
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)

            # Create Student Profile
            student = Student.objects.create(
                user=user,
                father_name=father_name,
                name_of_guru=guru_name,
                guru_mobile_number=guru_mobile_number,
                guru_registration_number=guru_reg_num,
                name_of_institute=name_of_institute,
                payment_ref_no=payment_ref_number,
                payment_proof=payment_proof,
            )

            # Guru-Student Association
            if guru_reg_num:
                try:
                    guru = Guru.objects.get(reg_num=guru_reg_num)
                    association, created = GuruStudentAssociation.objects.get_or_create(guru=guru)
                    association.students.add(student)
                except Guru.DoesNotExist:
                    raise ValidationError("Invalid Guru Registration Number.")

            context['success_message'] = "Student registered successfully!"
            context['reg_num'] = student.reg_num

        except ValidationError as e:
            context['error_message'] = str(e)
        except Exception as e:
            print(f"Unexpected error: {e}")  # Log the error for debugging
            context['error_message'] = "An unexpected error occurred. Please try again."

    return render(request, 'backend/studentRegistration.html', context)


@transaction.atomic
def bulkRegistration(request):
    context = {'form_data': {}, 'error_message': {}}

    if request.method == 'POST':
        # Extract Guru Details
        reg_num = request.POST.get('reg_num')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        payment_ref_number = request.POST.get('payment_ref_number')
        proof = request.FILES.get('proof')

        # Preserve form data in context
        context['form_data'] = {
            'reg_num': reg_num,
            'mobile_number': mobile_number,
            'email': email,
            'payment_ref_number': payment_ref_number,
        }

        # Validate Guru details
        try:
            guru = Guru.objects.get(reg_num=reg_num)
        except ObjectDoesNotExist:
            context['error_message']['guru'] = "Invalid Guru details. Please verify your credentials."
            return render(request, 'backend/bulkRegistration.html', context)

        # Validate payment details
        if not payment_ref_number:
            context['error_message']['payment_ref_number'] = "Payment reference number is required."
        if not proof:
            context['error_message']['proof'] = "Payment proof is required."

        if context['error_message']:
            return render(request, 'backend/bulkRegistration.html', context)

        # Process student details dynamically
        student_names = request.POST.getlist('student_name[]')
        student_mobile_numbers = request.POST.getlist('student_mobile_number[]')
        student_emails = request.POST.getlist('student_email[]')

        print(student_emails)

        if not student_names or not student_mobile_numbers or not student_emails:
            context['error_message']['students'] = "At least one student must be provided."
            return render(request, 'backend/bulkRegistration.html', context)

        try:
            students = []
            for i in range(len(student_names)):
                student_name = student_names[i]
                student_mobile = student_mobile_numbers[i]
                student_email = student_emails[i]

                if not student_name:
                    context['error_message'][f'name_{i}'] = f"Student {i + 1}: Name is required."
                if not student_mobile:
                    context['error_message'][f'mobile_{i}'] = f"Student {i + 1}: Mobile number is required."
                if not student_email:
                    context['error_message'][f'email_{i}'] = f"Student {i + 1}: Email is required."

                if context['error_message']:
                    return render(request, 'backend/bulkRegistration.html', context)

                if CustomUser.objects.filter(username=student_email).exists():
                    context['error_message'][f'email_{i}'] = f"Student {i + 1}: Email already exists."
                    continue

                # Create student user
                user = CustomUser.objects.create_user(
                    username=student_email,
                    email=student_email,
                    password="default_password123"
                )
                user.save()

                # Add user to 'Student' group
                student_group, created = Group.objects.get_or_create(name='Student')
                user.groups.add(student_group)

                # Create Student object
                student = Student.objects.create(
                    user=user,
                    mobile_number=student_mobile,
                    guru=guru
                )
                students.append(student)

            # Add entry in BulkRegistration
            bulk_registration = BulkStudentRegistration.objects.create(
                guru=guru,
                payment_ref_number=payment_ref_number,
                payment_proof=proof
            )
            bulk_registration.students.add(*students)

            messages.success(request, "Group Registration successful.")
            return redirect('guru_registration')

        except Exception as e:
            print(e)
            context['error_message']['general'] = f"An error occurred: {e}"
            return render(request, 'backend/bulkRegistration.html', context)

    return render(request, 'backend/bulkRegistration.html', context)
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Guru, Student, GuruStudentAssociation

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
                # Extract CustomUser fields from POST data
                name = request.POST.get('name')
                email = request.POST.get('email')
                mobile_number = request.POST.get('mobile_number')
                profile_photo = request.POST.get('profile')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                name_of_institute = request.POST.get('name_of_institute')
                address_of_institute = request.POST.get('address_of_institute')

                # Retain form data for repopulation in case of errors
                context['form_data'] = {
                    'name': name,
                    'email': email,
                    'mobile_number': mobile_number,
                    'profile': profile_photo,
                    'name_of_institute': name_of_institute,
                    'address_of_institute': address_of_institute,
                }

                # Validate required fields
                if not all([name, email, mobile_number, profile_photo, password, confirm_password,
                            name_of_institute, address_of_institute]):
                    messages.error(request, "All fields are required.")
                    return render(request, 'guru_register.html', context)

                # Validate password confirmation
                if password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return render(request, 'guru_register.html', context)

                # Create CustomUser
                user = CustomUser.objects.create(
                    name=name,
                    email=email,
                    mobile_number=mobile_number,
                    password=make_password(password),
                    role='TEACHER'
                )

                # Create Guru
                guru = Guru.objects.create(
                    user=user,
                    name_of_institute=name_of_institute,
                    address_of_institute=address_of_institute,
                    profile_photo=profile_photo
                )

                # Success Message
                messages.success(request, f"Registration successful! Your registration number is {guru.reg_num}.")
                context['success'] = True

        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")

    return render(request, "backend/guruRegistration.html", context)


def studentRegistration(request):
    context = {}

    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        guru_name = request.POST.get('guru_name')
        guru_mobile_number = request.POST.get('guru_mobile_number')
        guru_reg_num = request.POST.get('guru_reg_num')
        name_of_institute = request.POST.get('name_of_institue')
        payment_ref_number = request.POST.get('payment_ref_number')
        payment_proof_url = request.POST.get('payment_proof_url')

        # Validation checks
        try:
            if password != confirm_password:
                raise ValidationError("Passwords do not match")

            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError("Email already registered")

            if CustomUser.objects.filter(mobile_number=mobile_number).exists():
                raise ValidationError("Mobile number already registered")

            if Student.objects.filter(payment_ref_no=payment_ref_number).exists():
                raise ValidationError("Payment reference number already used")

            # Create CustomUser
            user = CustomUser.objects.create(
                name=name,
                email=email,
                mobile_number=mobile_number,
                password=make_password(password),
                role='STUDENT',
            )

            # Create Student Profile
            student = Student.objects.create(
                user=user,
                dob=dob,
                father_name=father_name,
                mother_name=mother_name,
                name_of_guru=guru_name,
                guru_mobile_number=guru_mobile_number,
                guru_registration_number=guru_reg_num,
                name_of_institute=name_of_institute,
                payment_ref_no=payment_ref_number,
                payment_proof=payment_proof_url,
            )

            # Guru Association
            if guru_reg_num:
                try:
                    guru = Guru.objects.get(reg_num=guru_reg_num)
                    guruStudentAssociation = GuruStudentAssociation.objects.get(guru=guru)
                    guruStudentAssociation.students.add(student)
                except Guru.DoesNotExist:
                    raise ValidationError("Invalid Guru Registration Number")

            context['success_message'] = "Student registered successfully!"

        except ValidationError as e:
            context['error_message'] = str(e)
        except Exception as e:
            context['error_message'] = "An unexpected error occurred. Please try again."

        # Return the same template with the context
        return render(request, 'backend/studentRegistration.html', {'context': context})

    # GET request: Just render the template with empty fields
    return render(request, 'backend/studentRegistration.html', {'context': context})
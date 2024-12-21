from django.db import transaction
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.models import CustomUser, Student, Guru, GuruStudentAssociation
from .serializers import (
    CustomUserSerializer, CustomUserCreateSerializer,
    StudentSerializer, StudentCreateSerializer,
    GuruSerializer, GuruStudentAssociationSerializer,
    GuruStudentAssociationCreateSerializer
)


# API for creating users
class CustomUserCreateView(generics.CreateAPIView):
    serializer_class = CustomUserCreateSerializer


# API for listing and retrieving users
class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# API for Guru
class GuruViewSet(viewsets.ModelViewSet):
    queryset = Guru.objects.all()
    serializer_class = GuruSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# API for Student
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = StudentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# API for Guru-Student Association
class GuruStudentAssociationViewSet(viewsets.ModelViewSet):
    queryset = GuruStudentAssociation.objects.all()
    serializer_class = GuruStudentAssociationSerializer

    def create(self, request, *args, **kwargs):
        serializer = GuruStudentAssociationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# List students associated with a specific guru
class GuruStudentsListView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        guru_id = self.kwargs['guru_id']
        return Student.objects.filter(guru_registration_number=guru_id)
# @method_decorator(csrf_exempt, name='dispatch')
# @csrf_exempt
class StudentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract the data from the request
        data = request.data

        # Separate the `CustomUser` fields
        custom_user_data = {
            "name": data.get("name"),
            "mobile_number": data.get("mobile_number"),
            "email": data.get("email"),
            "password": data.get("password"),
        }

        # Validate password confirmation
        if data.get("password") != data.get("confirm_password"):
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create `CustomUser` object
            user_serializer = CustomUserCreateSerializer(data=custom_user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            # Prepare the `Student` data
            student_data = {
                "user": user.id,
                "dob": data.get("dob"),
                "father_name": data.get("father_name"),
                "mother_name": data.get("mother_name"),
                "guru_name": data.get("guru_name"),
                "guru_registration_number": data.get("guru_reg_num"),
                "name_of_institute": data.get("name_of_institute"),
                "guru_mobile_number": data.get("guru_mobile_number"),
                "address_of_institute": data.get("address_of_institute"),
                "payment_ref_no": data.get("payment_ref_number"),
                "payment_proof": data.get("payment_proof_url"),
            }

            # Create `Student` object
            student_serializer = StudentCreateSerializer(data=student_data)
            student_serializer.is_valid(raise_exception=True)
            student = student_serializer.save()

        # Return the created `Student` object
        return Response(student_serializer.data, status=status.HTTP_201_CREATED)
# @method_decorator(csrf_exempt, name="dispatch")
class GuruCreateView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # Extract the data from the request
        data = request.data

        # Separate the `CustomUser` fields
        custom_user_data = {
            "name": data.get("name"),
            "mobile_number": data.get("mobile_number"),
            "email": data.get("email"),
            "password": data.get("password"),
        }

        # Validate password confirmation
        if data.get("password") != data.get("confirm_password"):
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create `CustomUser` object
            user_serializer = CustomUserCreateSerializer(data=custom_user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

            # Prepare the `Guru` data
            guru_data = {
                "user": user.id,
                # "guru_reg_num": data.get("guru_reg_num"),
                "name_of_institute": data.get("name_of_institute"),
                "address_of_institute": data.get("address_of_institute"),
                # "specialization": data.get("specialization"),
                # "experience_years": data.get("experience_years"),
            }

            # Create `Guru` object
            guru_serializer = GuruSerializer(data=guru_data)
            guru_serializer.is_valid(raise_exception=True)
            guru = guru_serializer.save()

        # Return the created `Guru` object
        return Response(guru_serializer.data, status=status.HTTP_201_CREATED)

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})
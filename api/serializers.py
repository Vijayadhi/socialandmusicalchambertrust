from rest_framework import serializers
from backend.models import CustomUser, Student, Guru, GuruStudentAssociation


# Serializer for creating and retrieving CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'name', 'email', 'mobile_number', 'alternate_number', 'role',
            'is_active', 'is_verified', 'reg_date'
        ]
        read_only_fields = ['is_active', 'reg_date']


# Serializer for creating a new user with password
class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'name', 'email', 'mobile_number', 'alternate_number', 'role',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            alternate_number=validated_data.get('alternate_number', ''),
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user


# Serializer for Guru
class GuruSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Guru
        fields = [
            'id', 'user', 'reg_num', 'name_of_institute',
            'address_of_institute', 'profile_photo'
        ]


# Serializer for Student
class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'reg_num', 'dob', 'grade_studying', 'father_name',
            'mother_name', 'name_of_guru', 'guru_mobile_number',
            'guru_registration_number', 'name_of_institute',
            'address_of_institute', 'payment_ref_no', 'payment_proof'
        ]


# Serializer for creating a Student
class StudentCreateSerializer(serializers.ModelSerializer):
    user = CustomUserCreateSerializer()

    class Meta:
        model = Student
        fields = [
            'user', 'dob', 'grade_studying', 'father_name',
            'mother_name', 'name_of_guru', 'guru_mobile_number',
            'guru_registration_number', 'name_of_institute',
            'address_of_institute', 'payment_ref_no', 'payment_proof'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


# Serializer for Guru-Student Association
class GuruStudentAssociationSerializer(serializers.ModelSerializer):
    guru = GuruSerializer()
    students = StudentSerializer(many=True)

    class Meta:
        model = GuruStudentAssociation
        fields = ['id', 'guru', 'students']


# Serializer for adding students to a Guru-Student Association
class GuruStudentAssociationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuruStudentAssociation
        fields = ['guru', 'students']

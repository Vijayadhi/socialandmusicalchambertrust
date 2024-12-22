from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from backend.models import CustomUser, Guru, GuruStudentAssociation, Student


# Register your models here.
class CustomUserInline(admin.StackedInline):
    model = CustomUser
    fields = ('email', 'password', 'name', 'mobile_number', 'is_active', )
    extra = 1  # This allows you to add new instances of CustomUser
    readonly_fields = ('email', 'password', 'is_active',)  # Remove 'is_verified' from here
    can_delete = False
    show_change_link = True  # Allow a link to change the user directly

admin.site.unregister(Group)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    # Default fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'mobile_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser','groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fieldsets for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile_number', 'password1', 'password2', 'is_superuser')}
         ),
    )

    def get_fieldsets(self, request, obj=None):
        """
        Conditionally exclude the 'groups' field if the user is not in 'CustomAdmin' group.
        """
        fieldsets = super().get_fieldsets(request, obj)

        # If the current user is not in the "CustomAdmin" group, remove 'groups' field from fieldsets
        if not(request.user.groups.filter(name='CustomAdmin').exists()):
            # Modify the permissions fieldset to remove 'groups'
            fieldsets = [

                ('Permissions', {'fields': ('is_staff', 'is_active', )}),
            ]
            # fieldsets[1] = })

        return fieldsets


    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Only allow users with the "Custom Admin" group to view all users
        if request.user.groups.filter(name='CustomAdmin').exists():
            return queryset
        # else:
        #     # Restrict users from viewing all groups

        # Otherwise, restrict to the current user's record
        return queryset.filter(email=request.user.email)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name="CustomAdmin"):
            return True
        """
        Disable the delete button for all users, effectively hiding the delete functionality.
        """
        return False

# admin.site.unregister(Group)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'reg_num', 'grade_studying', 'guru_registration_number', 'is_verified')
    search_fields = ('user__username', 'reg_num', 'guru_registration_number')
    list_filter = ('grade_studying', 'is_verified')

    # inlines = [CustomUserInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Save the student object first

        # Associate the student with the guru if a guru_registration_number is provided
        if obj.guru_registration_number:
            try:
                guru = Guru.objects.get(reg_num=obj.guru_registration_number)
                association, created = GuruStudentAssociation.objects.get_or_create(guru=guru)
                if not association.students.filter(id=obj.id).exists():
                    association.students.add(obj)
            except Guru.DoesNotExist:
                self.message_user(request, "Invalid Guru Registration Number: Guru not found.", level="error")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Check if the user is a Guru
        if request.user.groups.filter(name='Guru').exists():
            # Show only the students associated with this guru
            return queryset.filter(
                guru_registration_number__in=GuruStudentAssociation.objects.filter(guru__user=request.user).values(
                    'guru__reg_num'), email=request.user.email)

        return queryset

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name="CustomAdmin"):
            return True
        """
        Disable the delete button for all users, effectively hiding the delete functionality.
        """
        return False

    class Media:
        js = ('admin/js/delete.js',)


@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'reg_num', 'user_name', 'user_phone', 'is_verified', 'registration_date')
    list_filter = ('is_verified', 'user__reg_date')
    search_fields = ('user__email', 'reg_num', 'user__name', 'user__mobile_number')

    # Inline the CustomUser form
    # inlines = [CustomUserInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'reg_num', 'name_of_institute', 'address_of_institute', 'profile_photo')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
    )

    @admin.display(ordering='user__email', description='Email')
    def user_email(self, obj):
        return obj.user.email

    @admin.display(ordering='user__name', description='Name')
    def user_name(self, obj):
        return obj.user.name

    @admin.display(ordering='user__mobile_number', description='Phone Number')
    def user_phone(self, obj):
        return obj.user.mobile_number

    @admin.display(ordering='user__reg_date', description='Registration Date')
    def registration_date(self, obj):
        return obj.user.reg_date

    @admin.display(ordering='is_verified', description='Verified')
    def is_verified(self, obj):
        return obj.is_verified

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Check if the user is a guru, if so, filter the queryset to show only their profiles
        if request.user.groups.filter(name='Guru').exists():
            # Show only the guru's profile and profiles of the students they added
            return queryset.filter(user=request.user)

        return queryset

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name="CustomAdmin"):
            return True
        """
        Disable the delete button for all users, effectively hiding the delete functionality.
        """
        return False

# Registering CustomUserAdmin with the admin site
# admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(GuruStudentAssociation)
class GuruStudentAssociationAdmin(admin.ModelAdmin):
    list_display = ('guru_name', 'guru_email', 'guru_reg_num', 'number_of_students')
    search_fields = ('guru__user__email', 'guru__reg_num', 'guru__user__name', 'guru__user__mobile_number')
    list_filter = ('guru__user__reg_date',)

    # Custom methods for displaying related fields
    @admin.display(ordering='guru__user__name', description='Guru Name')
    def guru_name(self, obj):
        return obj.guru.user.name

    @admin.display(ordering='guru__user__email', description='Guru Email')
    def guru_email(self, obj):
        return obj.guru.user.email

    @admin.display(ordering='guru__reg_num', description='Guru Registration Number')
    def guru_reg_num(self, obj):
        return obj.guru.reg_num

    @admin.display(description='Number of Students')
    def number_of_students(self, obj):
        return obj.students.count()

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name="CustomAdmin"):
            return True
        """
        Disable the delete button for all users, effectively hiding the delete functionality.
        """
        return False
# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(TeacherStudentRegistration)
# admin.site.register(Student, StudentAdmin)
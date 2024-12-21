from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserCreateView, CustomUserViewSet,
    GuruViewSet, StudentViewSet,
    GuruStudentAssociationViewSet, GuruStudentsListView, GuruCreateView, StudentCreateView, get_csrf_token
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'guru', GuruViewSet, basename='guru')
router.register(r'student', StudentViewSet, basename='student')
router.register(r'associations', GuruStudentAssociationViewSet, basename='association')

urlpatterns = [
    path('create-user/', CustomUserCreateView.as_view(), name='create-user'),
    path('guru/<int:guru_id>/students/', GuruStudentsListView.as_view(), name='guru-students'),
    path('guru/register', GuruCreateView.as_view()),
    path('student/register', StudentCreateView.as_view(), name='create_student'),
    path('srf-token/', get_csrf_token, name='csrf_token'),
    path('', include(router.urls)),
]

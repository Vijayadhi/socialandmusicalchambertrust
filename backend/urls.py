from django.urls import path

from backend.views import registerGuru, studentRegistration

urlpatterns = [
    path('registerGuru', registerGuru),
    path('studentRegistration', studentRegistration)
]
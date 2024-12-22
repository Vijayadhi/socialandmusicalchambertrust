from django.urls import path

from backend.views import registerGuru, studentRegistration, bulkRegistration

urlpatterns = [
    path('registerGuru', registerGuru),
    path('studentRegistration', studentRegistration),
    path('groupRegistration', bulkRegistration),
]

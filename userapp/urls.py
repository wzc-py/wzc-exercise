from django.urls import path

from userapp import views

urlpatterns = [
    path("users/", views.UserAPIView.as_view()),
    path("employees/", views.EmployeeAPIView.as_view()),
    path("employees/<str:id>/", views.EmployeeAPIView.as_view()),
]

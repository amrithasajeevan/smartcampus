from django.urls import path
from .views import *
urlpatterns = [
    path('register/',RegisterAPIView.as_view(),name='regg'),
    path('login/',LoginView.as_view(),name='login'),
    path('add-attendance/<str:admission_number>/', AddAttendance.as_view(), name='add_attendance'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
    path('view-attendance/', ViewAttendance.as_view(), name='view_attendance'),
    ]
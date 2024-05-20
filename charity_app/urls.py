from django.contrib import admin
from django.urls import path

from charity_app.views import (LandingPageView, AddDonationView, RegisterView, LoginView, LogoutView,
                               UserDetailView)

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('add-donation/', AddDonationView.as_view(), name='add-donation'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-details/<int:pk>/', UserDetailView.as_view(), name='user-details'),
]
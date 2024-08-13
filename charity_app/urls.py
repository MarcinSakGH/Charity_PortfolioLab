from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView

from charity_app.views import (LandingPageView, AddDonationView, RegisterView, LoginView, LogoutView,
                               UserDetailView, FormConfirmationView, UpdateDonationStatus,
                               UserUpdateView)

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('add-donation/', AddDonationView.as_view(), name='add-donation'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-details/<int:pk>/', UserDetailView.as_view(), name='user-details'),
    path('form-confirmation/', FormConfirmationView.as_view(), name='form-confirmation'),
    path('update_donation_status/', UpdateDonationStatus.as_view(), name='update_donation_status'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
]
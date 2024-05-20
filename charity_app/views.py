from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View, DetailView
from .models import Donation, Institution, Category
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class LandingPageView(View):
    def get(self, request):
        total_bags_quantity = Donation.total_quantity_of_bags()
        number_of_institutions = Institution.count_institutions()
        local_organisations = Institution.objects.filter(type=3)
        non_government_organisations = Institution.objects.filter(type=2)
        foundations = Institution.objects.filter(type=1)
        ctx = {'total_bags_quantity': total_bags_quantity, 'number_of_institutions': number_of_institutions,
               'local_organisations': local_organisations, 'non_government_organisations': non_government_organisations,
               'foundations': foundations}
        return render(request, 'index.html', context=ctx)


class AddDonationView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {'categories': categories, 'institutions': institutions}
        return render(request, 'form.html', context=ctx)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            messages.info(request, 'Brak użytkownika w bazie danych')
            return render(request, 'register.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        if password != confirm_password:
            error_message = 'Passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})
        new_user = User.objects.create_user(
            username=email, first_name=name, last_name=surname, email=email, password=password)
        return redirect('login')


class UserDetailView(DetailView):
    model = User
    template_name = 'userpage.html'

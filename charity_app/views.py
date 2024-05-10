from django.shortcuts import render
from django.views.generic import View
from .models import Donation, Institution

# Create your views here.


class LandingPageView(View):
    def get(self, request):
        total_bags_quantity = Donation.total_quantity_of_bags()
        number_of_institutions = Institution.count_institutions()
        ctx = {'total_bags_quantity': total_bags_quantity, 'number_of_institutions': number_of_institutions}
        return render(request, 'index.html', context=ctx)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
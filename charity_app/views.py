from django.shortcuts import render
from django.views.generic import View
from .models import Donation, Institution

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


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
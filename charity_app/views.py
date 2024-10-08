from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
import json
from django.contrib import messages
from django.views.generic import View, DetailView, UpdateView
from .models import Donation, Institution, Category
from django.contrib.auth.models import User
from .forms import UserUpdateForm

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

    def post(self, request):
        quantity = int(request.POST.get('bags'))
        selected_categories = request.POST.getlist('categories')
        categories = Category.objects.filter(name__in=selected_categories)
        institution_id = request.POST.get('institution')
        institution = Institution.objects.get(id=institution_id)
        new_donation = Donation(quantity=quantity, institution=institution, user=request.user,
                                address=request.POST.get('address'),
                                city=request.POST.get('city'), zip_code=request.POST.get('postcode'),
                                pick_up_date=request.POST.get('date'), pick_up_time=request.POST.get('time'),
                                pick_up_comment=request.POST.get('more_info'))
        new_donation.save()

        new_donation.categories.set(categories)

        new_donation.save()

        return redirect('form-confirmation')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donations'] = Donation.objects.filter(user=self.request.user).order_by('is_taken')
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('landing')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def get_object(self, queryset=None):
        return self.request.user

class FormConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UpdateDonationStatus(View):
    def post(self, request):
        data = json.loads(request.body)
        donation_id = data['donation_id']
        is_taken = data['is_taken']

        if donation_id is not None:
            try:
                donation = Donation.objects.get(id=donation_id)
                donation.is_taken = is_taken
                donation.save()

                return JsonResponse({'status': 'success'}, status=200)
            except Donation.DoesNotExist:
                return JsonResponse({'errot': 'donation not found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid or missing donation id'}, status=400)
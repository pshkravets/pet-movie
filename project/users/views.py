from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.conf import settings


from .forms import CustomUserCreationForm, LoginUserForm, OtpForm
from .models import User
from .utils import send_otp_email

class SignUpView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        data = form.cleaned_data

        self.request.session['email'] = data['email']
        if User.objects.exist(data['email']):
            user = User.objects.get(email=data['email'])
            if user.is_active:
                messages.error(self.request, 'User with this email already exist')
                return redirect(reverse_lazy('authorization'))
            messages.error(self.request, 'You created account but didn\'t activate email')
            return redirect(reverse_lazy('activate'))
        if not form.password_validation():
            messages.error(self.request, 'Passwords are not the same')
            return redirect(reverse_lazy('authorization'))
        user = User.objects.create_user(email=data['email'], password=data['password1'], is_active=False)
        otp = user.generate_otp()
        send_otp_email(user.email, otp)
        return redirect(reverse_lazy('activate'))


class AccountActivateView(FormView):
    form_class = OtpForm
    template_name = 'users/otp_checkout.html'

    def form_valid(self, form):
        data = form.cleaned_data
        email = self.request.session['email']
        user = User.objects.get(email=email)
        if user.checkout_otp(data['otp']):
            user.is_active = True
            user.save()
            messages.success(self.request, 'We succesfuly created account')
            return redirect(reverse_lazy('login_user'))

        if timezone.now() > user.otp_exparation:
            messages.error(self.request, 'Your OTP expired')
        messages.error(self.request, 'Your OTP is wrong')
        return redirect(reverse_lazy('activate'))


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def form_valid(self, form):
        data = form.cleaned_data
        if User.objects.exist(data['email']):
            user = User.objects.get(email=data['email'])
            if not user.is_active:
                messages.error(self.request, 'You shoul activate your account')
                return redirect(reverse_lazy('activate'))
        user = authenticate(self.request, email=data['email'], password=data['password'])
        if user is None:
            messages.error(self.request, 'Invalid email or password')
            return redirect(reverse_lazy('login_user'))
        login(self.request, user)
        return redirect(reverse_lazy('movie-list'))

def send_otp_view(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    user.generate_otp()
    send_otp_email(user.email, user.otp)
    return redirect(reverse_lazy('activate'))

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('movie-list'))

class HemePageView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self):
        context = super().get_context_data()
        return context

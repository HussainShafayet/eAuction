from django.shortcuts import render, redirect
from accounts.forms import Register, UserLoginForm
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# forgot password
from django.contrib.auth.views import PasswordChangeForm, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import EmailMessage


# Create your views here.

def home(request):
    val = 'home'
    return render(request, 'home.html', {'val': val})


# User_Registration
def sign_up(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            get_email = User.objects.filter(email=email)
            for i in get_email:
                if i.email == email:
                    messages.warning(request, 'Email already exists.')
                    context = {
                        'form': form
                    }
                    return render(request, 'register.html', context)
                    break
            user = form.save()
            user_profile = Profile(user=user)
            user_profile.save()
            messages.success(request, 'Account Created Successfully.')
            return redirect('login')
        else:
            context = {
                'form': form,
            }
            return render(request, 'register.html', context)
    else:
        form = Register()
        context = {
            'form': form,
        }
        return render(request, 'register.html', context)


# User Login
def user_login(request):
    if request.method == 'POST':
        log_form = UserLoginForm(request.POST)
        if log_form.is_valid():
            email = log_form.cleaned_data['email']
            password = log_form.cleaned_data['password']
            username = User.objects.filter(email=email)
            if not username:
                messages.warning(
                    request, 'Not Found this email. Please Sign Up First.')
                context = {
                    'log_form': UserLoginForm(),

                }
                return render(request, 'login.html', context)
            else:
                for i in username:
                    username2 = i
                user = authenticate(username=username2, password=password)
                if user:
                    login(request, user)
                    messages.success(request, 'Login Successfully')
                    return redirect('/')
                else:
                    messages.warning(request, 'Username or Password Incorrect')
                    context = {
                        'log_form': UserLoginForm(),

                    }
                    return render(request, 'login.html', context)
        else:
            messages.warning(request, 'Username or Password Incorrect')
            context = {
                'log_form': UserLoginForm(),

            }
            return render(request, 'login.html', context)
    else:
        log_form = UserLoginForm()
        context = {
            'log_form': log_form
        }
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'You are logged out')
    return redirect('/')


# Reset Password
class ResetPassword(UserPassesTestMixin, PasswordResetView):
    template_name = 'password_reset.html'

    def test_func(self):
        return self.request.user.is_anonymous


class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class ResetPasswordComplete(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

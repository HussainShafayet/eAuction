from django.shortcuts import render, redirect
from accounts.forms import Register, UserLoginForm, Profile_edit_Form, Profile_form
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


def profile(request):
    current_user = request.user
    user = User.objects.get(username=current_user)
    profile_details = 'profile_details'
    context = {
        'user': user,
        'profile_details': profile_details
    }
    return render(request, 'profile.html', context)


def profile_edit(request, id):
    if request.method == 'POST':
        form = Profile_edit_Form(request.POST, instance=request.user)
        form2 = Profile_form(request.POST or None, request.FILES or None, instance=request.user.profile)
        if form.is_valid() and form2.is_valid():
            form.save()
            profile = Profile.objects.get(user=request.user)
            image = profile.image
            if str(image) in '/images/profile/profile.png':
                form2.save()
                messages.success(request, 'Profile update success')
                return redirect('profile')
            else:
                image.delete()
                form2.save()
                messages.success(request, 'Profile update success')
                return redirect('profile')
        else:
            messages.warning(request, 'Try again')
            context = {
                'form': form,
                'form2': form2

            }
            return render(request, 'profile.html', context)
    else:
        form = Profile_edit_Form(instance=request.user)
        form2 = Profile_form()
        context = {
            'form': form,
            'form2': form2

        }
    return render(request, 'profile.html', context)


def password_change(request, id):
    if request.method == 'POST':
        current_user = User.objects.get(id=id)
        password_form = PasswordChangeForm(
            data=request.POST, user=current_user)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, 'Password change successfully!')
            update_session_auth_hash(request, password_form.user)
            return redirect('profile')
        else:
            messages.warning(request, 'Try again!')
            val = 'password_change'
            context = {
                'password_form': password_form,
                'user': current_user,
                'val': val,
            }
            return render(request, 'profile.html', context)
    else:
        current_user = User.objects.get(id=id)
        password_form = PasswordChangeForm(user=current_user)
        val = 'password_change'
        context = {
            'password_form': password_form,
            'user': current_user,
            'val': val,
        }
        return render(request, 'profile.html', context)

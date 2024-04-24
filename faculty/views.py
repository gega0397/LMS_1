from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from faculty.models import CustomUser
from faculty.forms import CustomUserCreationForm, LoginForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        # Create a form that has request.POST
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the user's password securely
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 == password2:
                user.set_password(password1)
                user.save()

                messages.success(request, f'Your Account has been created {email} ! Proceed to log in')
                login(request, user)
                return redirect('faculty:profile')  # Redirect to the login page
            else:
                # Handle password mismatch error here
                form.add_error('password2', 'Passwords entered do not match')
    else:
        form = CustomUserCreationForm()
    return render(request, 'faculty/register.html', {'form': form})


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect('faculty:profile')
            else:
                form.add_error(field=None, error="Invalid username or password")

    return render(request, 'faculty/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user

    if user.is_student():
        return render(request, 'student_profile.html', {'user': user})
    if user.is_lecturer():
        return render(request, 'lecturer_profile.html',  {'user': user})

from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib import messages

from django.http import HttpResponse


# Create your views here.

def register(request):
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
                return redirect('faculty:login')  # Redirect to the login page
            else:
                # Handle password mismatch error here
                form.add_error('password2', 'Passwords entered do not match')
    else:
        form = CustomUserCreationForm()
    return render(request, 'faculty/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        # if form.is_valid():
        #     # authenticate
        #     # login
        #     return redirect('profile')
        pass
    return HttpResponse('Login page')
    #return render(request, 'faculty/login.html')


def profile(request):
    if not request.user.is_authenticated():
        return redirect('login')
    if request.user.is_student():
        return render(request, 'student_profile.html')
    if request.user.is_lecturer():
        return render(request, 'lecturer_profile.html')

from django.shortcuts import render,redirect
from .models import CustomUser

# Create your views here.

def register(request):
    if request.method == 'POST':
        if for.is_valid():
            form.save()

            # CustomUser -> PK
            # StudentFaculty -> student, faculty

    # html, if user_type = Student -> faculty
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        if form.is_valid():
            # authenticate
            # login
            return redirect('profile')
    return render(request, 'login.html')


def profile(request):
    if not request.user.is_authenticated():
        return redirect('login')
    if request.user.is_student():

        return render(request, 'student_profile.html')
    if request.user.is_lecturer():
        return render(request, 'lecturer_profile.html')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from faculty.models import CustomUser, StudentFaculty, Classroom, StudentSubject, Homework
from faculty.forms import CustomUserCreationForm, LoginForm, StudentProfileForm, ClassroomCreationForm, HomeworkForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from faculty.choices import MAX_CLASSROOM_SIZE, IS_OPEN_TO_CHOOSE, MAX_STUDENT_CLASSROOM


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
        student_faculty = StudentFaculty.objects.filter(student=user.id).first()
        print(student_faculty, user.id)
        form = StudentProfileForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user
            obj.save()
            return redirect('faculty:profile')

        subjects = []
        if student_faculty and student_faculty.faculty:
            subjects = student_faculty.faculty.subjects.all()

        classrooms = Classroom.objects.filter(subject__in=subjects).exclude(studentsubject__student=user.id)
        enrolled_classrooms = StudentSubject.objects.filter(student=user.id)

        context = {
            'user': user,
            'form': form,
            'subjects': subjects,
            'classrooms': classrooms,
            'faculty': student_faculty,
            'enrolled_classrooms': enrolled_classrooms,
            'max_classroom': MAX_STUDENT_CLASSROOM,
            'is_open_to_choose': IS_OPEN_TO_CHOOSE,
        }
        return render(request, 'faculty/student_profile.html', context)

    if user.is_lecturer():
        form = ClassroomCreationForm(request.POST, request.FILES)
        if request.method == 'POST' and form.is_valid():
            classroom = form.save(commit=False)
            classroom.lecturer = user
            classroom.save()
            classroom.subject_id = form.cleaned_data['subject'].id
            return redirect('faculty:profile')

        classrooms = Classroom.objects.filter(lecturer=user)

        context = {
            'user': user,
            'form': form,
            'classrooms': classrooms,
        }
        return render(request, 'faculty/lecturer_profile.html', context)


@login_required
def classroom_view(request, classroom_id):
    user = request.user
    classroom = get_object_or_404(Classroom, id=classroom_id)

    if user.is_student():
        student_enrollment = StudentSubject.objects.filter(student=user, classroom=classroom).first()
        if not student_enrollment:
            messages.error(request, 'You are not enrolled in this classroom.')
            return redirect('faculty:profile')
        syllabus = classroom.syllabus
        return render(request, 'faculty/classroom_view.html', {'classroom': classroom, 'syllabus': syllabus})

    if user.is_lecturer():
        if classroom.lecturer != user:
            messages.error(request, 'You are not the lecturer for this classroom.')
            return redirect('faculty:profile')

        enrolled_students = classroom.studentsubject_set.all()
        form1 = HomeworkForm

        return render(request, 'faculty/lecturer_classroom_view.html', {
            'classroom': classroom,
            'enrolled_students': enrolled_students,
            'form1': form1
        })

    messages.error(request, 'You are not authorized to view this classroom.')
    return redirect('faculty:profile')


@login_required
def join_classroom(request, classroom_id):
    user = request.user
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    if user.is_student():
        if classroom.is_full:
            # Classroom is full, display an error message
            messages.error(request, 'The classroom is full. You cannot join.')
        elif StudentSubject.objects.filter(student=user, classroom=classroom).exists():
            # Student has already joined this classroom
            messages.error(request, 'You have already joined this classroom.')
        else:
            # Student can join the classroom
            student_subject = StudentSubject.objects.create(student=user, classroom=classroom)

            # If the classroom is now full, mark it as full
            if classroom.studentsubject_set.count() >= classroom.max_students:
                classroom.is_full = True
                classroom.save()

            messages.success(request, 'You have successfully joined the classroom.')

    return redirect('faculty:profile')


@login_required
def homework_view(request, classroom_id):
    homeworks = Homework.objects.filter(classroom_id=classroom_id).order_by('-is_active', '-due_date')

    if request.user.is_student():
        pass

    create_homework = HomeworkForm()
    if request.method == "POST":
        create_homework = HomeworkForm(request.POST)
        if create_homework.is_valid():
            homework = create_homework.save(commit=False)
            homework.save()
            return redirect('faculty:homework')

    return render(request, 'faculty/homework.html', {'homeworks': homeworks, 'form': create_homework, 'user': request.user})


@login_required
def homework_detail(request, classroom_id, homework_id):
    homework = get_object_or_404(Homework, pk=homework_id)
    classroom = get_object_or_404(Classroom, id=classroom_id)
    student_list = Classroom.students.all
    lecturer = classroom.lecturer

    if request.user.is_student():
        pass

    if request.user != lecturer:
        redirect('faculty:profile')

    homework_form = HomeworkForm(instance=homework)

    if request.method == 'POST':
        homework_form = HomeworkForm(request.POST, instance=homework)
        if homework_form.is_valid():
            homework_form.save()

    return render(request, 'faculty/homework.html', {'homework_form': homework_form})
    # see submitted hw-s


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from faculty.models import CustomUser, StudentFaculty, Classroom, StudentSubject, Homework, StudentHomework
from faculty.forms import CustomUserCreationForm, LoginForm, StudentProfileForm, ClassroomCreationForm, HomeworkForm, \
    HomeworkSubmissionForm, ClassroomCalendarForm, StudentAttendanceForm, ClassroomAttendance, ClassroomCalendar
from django.conf import settings
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
        try:
            student_faculties = StudentFaculty.objects.filter(student=user.id)
            student_faculty = [student for student in student_faculties if student.status == 'active']
            if len(student_faculty):
                student_faculty = student_faculty[0]
            else:
                student_faculty = None
        except StudentFaculty.DoesNotExist:
            student_faculties = None
            student_faculty = None
        form = StudentProfileForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user
            obj.save()
            return redirect('faculty:profile')

        subjects = []
        if student_faculty and student_faculty.faculty:
            subjects = student_faculty.faculty.subjects.all()

        classrooms = Classroom.objects.filter(subject__in=subjects, is_full=False).exclude(students=user)

        enrolled_classrooms = Classroom.objects.filter(students=user)
        if settings.DEBUG: print(list(enrolled_classrooms))

        context = {
            'user': user,
            'form': form,
            'subjects': subjects,
            'classrooms': classrooms,
            'faculty': student_faculty,
            'faculties': student_faculties,
            'enrolled_classrooms': enrolled_classrooms,
            'max_classroom': MAX_STUDENT_CLASSROOM,
            'is_open_to_choose': IS_OPEN_TO_CHOOSE,
        }
        return render(request, 'faculty/student_profile.html', context)

    if user.is_lecturer():
        debug_mode = settings.DEBUG
        classroom_creation_form = ClassroomCreationForm(request.POST, request.FILES)
        if request.method == 'POST' and classroom_creation_form.is_valid():
            classroom = classroom_creation_form.save(commit=False)
            classroom.lecturer = user
            classroom.save()
            return redirect('faculty:profile')

        classrooms = Classroom.objects.filter(lecturer=user)

        context = {
            'user': user,
            'classroom_creation_form': classroom_creation_form,
            'classrooms': classrooms,
            'debug_mode': debug_mode,
        }
        return render(request, 'faculty/lecturer_profile.html', context)


@login_required
def classroom_view(request, classroom_id):
    user = request.user
    classroom = get_object_or_404(Classroom, id=classroom_id)
    calendar_form = ClassroomCalendarForm(classroom=classroom)
    debug = settings.DEBUG
    calendar = classroom.calendar.all()


    if user.is_student():
        student_enrollment = Classroom.objects.get(students=user, id=classroom.id)
        if not student_enrollment:
            messages.error(request, 'You are not enrolled in this classroom.')
            return redirect('faculty:profile')
        syllabus = classroom.syllabus
        return render(request, 'faculty/classroom_view.html', {'classroom': classroom, 'syllabus': syllabus})

    if user.is_lecturer():
        if classroom.lecturer != user:
            messages.error(request, 'You are not the lecturer for this classroom.')
            return redirect('faculty:profile')

        if request.method == 'POST':
            calendar_form = ClassroomCalendarForm(classroom, request.POST)
            if settings.DEBUG: print(calendar_form.is_valid())
            if calendar_form.is_valid():
                calendar_form.save(classroom)
                return redirect('faculty:classroom_view', classroom_id=classroom.id)
            else:
                if settings.DEBUG:
                    print(calendar_form.errors)

        enrolled_students = classroom.students.all()
        homework_form = HomeworkForm()

        return render(request, 'faculty/lecturer_classroom_view.html', {
            'classroom': classroom,
            'enrolled_students': enrolled_students,
            'homework_form': homework_form,
            'calendar_form': calendar_form,
            'calendar': calendar,
            'debug': debug,

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
        elif Classroom.objects.filter(students=user, id=classroom.id).exists():
            # Student has already joined this classroom
            messages.error(request, 'You have already joined this classroom.')
        else:
            # Student can join the classroom
            student_subject = classroom.students.add(user)
            if settings.DEBUG: print('added')
            # If the classroom is now full, mark it as full
            if classroom.students.count() >= classroom.max_students:
                classroom.is_full = True
                classroom.save()

            messages.success(request, 'You have successfully joined the classroom.')

    return redirect('faculty:profile')


def download_file(request, request_id):
    file = get_object_or_404(Classroom, pk=request_id)
    file_path = file.syllabus.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + 'syllabus'
    return response


@login_required
def homework_view(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    homeworks = Homework.objects.filter(classroom=classroom).order_by('-is_active', '-due_date')

    if request.user.is_student():
        student_enrollment = Classroom.objects.filter(students=request.user, id=classroom_id).exists()
        if not student_enrollment:
            messages.error(request, "You are not enrolled in this classroom.")
            return redirect('faculty:profile')
        return render(request, 'faculty/homework.html', {'homeworks': homeworks, 'classroom': classroom})

    if request.user.is_lecturer():
        if classroom.lecturer != request.user:
            messages.error(request, 'You are not the lecturer for this classroom.')
            return redirect('faculty:profile')

    homework_form = HomeworkForm()
    if request.method == "POST":
        homework_form = HomeworkForm(request.POST)
        if homework_form.is_valid():
            homework = homework_form.save(commit=False)
            homework.classroom = classroom
            homework.save()
            return redirect('faculty:homeworks', classroom_id=classroom.id)

    return render(request, 'faculty/homework.html', {'homeworks': homeworks,
                                                     'homework_form': homework_form,
                                                     'user': request.user,
                                                     'classroom': classroom,
                                                     })


@login_required
def homework_detail(request, classroom_id, homework_id):
    homework = get_object_or_404(Homework, pk=homework_id)
    classroom = get_object_or_404(Classroom, id=classroom_id)
    student_list = classroom.students.all()

    lecturer = classroom.lecturer

    if request.user.is_student():
        student_enrollment = Classroom.objects.filter(students=request.user, id=classroom_id).exists()
        if not student_enrollment:
            messages.error(request, "You are not enrolled in this classroom.")
            return redirect('faculty:profile')

        try:
            student_homework = StudentHomework.objects.get(student=request.user, homework=homework)
        except StudentHomework.DoesNotExist:
            student_homework = None

        if request.method == 'POST':
            form = HomeworkSubmissionForm(request.POST, instance=student_homework)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.student = request.user
                submission.homework = homework
                submission.save()
                messages.success(request, "Homework submitted successfully.")
                return redirect('faculty:homework_view', classroom_id=classroom.id)
        else:
            form = HomeworkSubmissionForm(instance=student_homework)

        return render(request, 'faculty/homework.html', {'form': form, 'homework': homework,
                                                         'classroom': classroom})

    if request.user != lecturer:
        redirect('faculty:profile')

    homework_form = HomeworkForm(instance=homework)

    if request.method == 'POST':
        homework_form = HomeworkForm(request.POST, instance=homework)
        if homework_form.is_valid():
            homework_form.save()

    return render(request, 'faculty/homework.html', {'homework_form': homework_form,
                                                     'classroom': classroom})
    # see submitted hw-s


@login_required
def create_homework(request):
    form = HomeworkForm()

    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save()
            homework.save()
            return redirect('faculty:homework_list')

    return render(request, 'faculty/create_homework.html', {'form': form})


@login_required
def homework_list(request):
    if request.method == 'GET':
        homeworks = Homework.objects.all()
        return render(request, 'faculty/all_homeworks.html', {'homeworks': homeworks})



@login_required
def attendance(request, classroom_id, attendance_id):
    attendance = get_object_or_404(ClassroomCalendar, pk=attendance_id)
    classroom = get_object_or_404(Classroom, id=classroom_id)
    student_list = classroom.students.all()
    lecturer = classroom.lecturer

    if not request.user == lecturer:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('faculty:profile')
    attendance_form = StudentAttendanceForm(attendance)

    if request.POST:
        attendance_form = StudentAttendanceForm(attendance, request.POST)
        if attendance_form.is_valid():
            attendance_form.save(attendance)
            messages.success(request, "Attendance submitted successfully.")
            return redirect('faculty:attendance', classroom_id=classroom.id, attendance_id=attendance_id)

    return render(request, 'faculty/attendance.html', {'attendance_form': attendance_form, 'title': 'attendance'})
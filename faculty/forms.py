from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from faculty.models import CustomUser, StudentFaculty, Faculty, Classroom, Subject, ClassroomAttendance, \
    ClassroomCalendar, \
    Homework
from faculty.choices import FORM_TYPE_CHOICES


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(choices=FORM_TYPE_CHOICES, required=False)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password-input'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    # Add a field for password strength
    password_strength = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ("email", 'user_type', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", 'user_type', 'first_name', 'last_name')


class LoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password-input'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    def clean(self):
        cleaned_data = super().clean()
        # Perform additional cleaning or validation as needed
        return cleaned_data


class StudentProfileForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=False)

    class Meta:
        model = StudentFaculty
        fields = ['faculty']


class JoinClassroomForm(forms.Form):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            faculties = StudentFaculty.objects.filter(student=user).values_list('faculty', flat=True)
            subjects = Subject.objects.filter(faculty__in=faculties)
            classrooms = Classroom.objects.filter(subject__in=subjects).exclude(studentsubject__student=user)
            self.fields['classroom'].queryset = classrooms


class ClassroomCreationForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    syllabus = forms.FileField(required=False)

    class Meta:
        model = Classroom
        fields = ['syllabus']


class ClassroomCalendarForm(forms.Form):
    def __init__(self, classroom, *args, **kwargs):
        super(ClassroomCalendarForm, self).__init__(*args, **kwargs)
        for i in range(classroom.number_of_classes):
            self.fields[f'date_{i}'] = forms.DateField(label=f'Date {i + 1}')
            self.fields[f'start_time_{i}'] = forms.TimeField(label=f'Start Time {i + 1}')
            self.fields[f'end_time_{i}'] = forms.TimeField(label=f'End Time {i + 1}')

    def save(self, classroom):
        for i in range(classroom.number_of_classes):
            date = self.cleaned_data[f'date_{i}']
            start_time = self.cleaned_data[f'start_time_{i}']
            end_time = self.cleaned_data[f'end_time_{i}']
            ClassroomCalendar.objects.create(
                classroom=classroom,
                date=date,
                start_time=start_time,
                end_time=end_time
            )


class StudentAttendanceForm(forms.Form):
    def __init__(self, classroom_calendar, *args, **kwargs):
        super(StudentAttendanceForm, self).__init__(*args, **kwargs)
        students = classroom_calendar.classroom_date.classroom.students.all()
        matching_instances = ClassroomAttendance.objects.filter(classroom_date=classroom_calendar)
        for student in students:
            try:
                matching_instance = matching_instances.get(student=student)
                initial_status = matching_instance.status  # Use the existing status if a match is found
            except ObjectDoesNotExist:
                initial_status = False

            self.fields[f'{student.id}'] = forms.BooleanField(
                label=f'{student}',
                required=False,
                initial=initial_status
            )

    def save(self, classroom_calendar):
        for student_id, value in self.cleaned_data.items():
            if value:
                student_attendance, created = ClassroomAttendance.objects.get_or_create(
                    classroom_date_id=classroom_calendar.id,
                    student_id=int(student_id),
                    defaults={'status': True}
                )
                if not created:
                    student_attendance.status = True
                    student_attendance.save()
            else:
                ClassroomAttendance.objects.filter(
                    classroom_date_id=classroom_calendar.id,
                    student_id=int(student_id),
                ).delete()


class HomeworkForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    due_date = forms.DateTimeField(label='Due Date', widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(label='Is Active', widget=forms.BooleanField())

    class Meta:
        model = Homework
        fields = ['title', 'description', 'due_date', 'is_active']

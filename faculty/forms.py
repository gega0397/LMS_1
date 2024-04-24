from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, StudentFaculty, Faculty, Classroom, Subject
from .choices import FORM_TYPE_CHOICES


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
        fields = ['faculty', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['faculty'].queryset = Faculty.objects.exclude(studentfaculty__student=user)


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

    class Meta:
        model = Classroom
        fields = ['subject']
USER_TYPE_CHOICES = (
    ('student', 'Student'),
    ('lecturer', 'Lecturer'),
    ('admin', 'Admin'),
)

USER_STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('graduated', 'Graduated'),
)

FORM_TYPE_CHOICES = (
    ('student', 'Student'),
    ('lecturer', 'Lecturer'),
)

MAX_CLASSROOM_SIZE = 20
MAX_STUDENT_CLASSROOM = 5
MAX_LECTURER_CLASSROOM = 10
IS_OPEN_TO_CHOOSE = True
DEFAULT_NUMBER_OF_CLASSES = 10
DEFAULT_LECTURE_DURATION = 2
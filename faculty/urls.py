from django.urls import path, re_path
from django.views.generic import RedirectView, TemplateView
from faculty.views import register_view, login_view, logout_view, profile_view, join_classroom, classroom_view, \
    download_file, homework_view, homework_detail, homework_list, create_homework

app_name = 'faculty'

urlpatterns = [
    path("", TemplateView.as_view(template_name="faculty/home.html"), name="home"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/homeworks/', homework_list, name='homework_list'),
    path('profile/homeworks/create/', create_homework, name='create_homework'),
    path('join_classroom/<int:classroom_id>', join_classroom, name='join_classroom'),
    path('classroom/<int:classroom_id>/', classroom_view, name='classroom_view'),
    path('download/<int:request_id>', download_file, name='download_file'),
    path('classroom/<int:classroom_id>/homework/', homework_view, name='homeworks'),
    path('classroom/<int:classroom_id>/homework/<int:homework_id>/', homework_detail, name='homework_detail'),
    path('classroom/<int:classroom_id>/homework/<int:homework_id>/submit/', homework_detail, name='homework_submission'),
    re_path(r'^.*$', RedirectView.as_view(pattern_name='faculty:home')),
]

from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from resume.views import login, registration, logout, searchUsers, updateprofile, viewprofile, updateresume, download, \
    addQuestion, getquestions, deletequestion, answerquestion, answerquestionaction, sendemail

urlpatterns = [

    path('admin/', admin.site.urls),

    path('',TemplateView.as_view(template_name = 'index.html'),name='login'),
    path('login/',TemplateView.as_view(template_name = 'index.html'),name='login'),
    path('loginaction/',login,name='loginaction'),

    path('registration/',TemplateView.as_view(template_name = 'registration.html'),name='registration'),
    path('regaction/',registration,name='regaction'),

    path('search/',TemplateView.as_view(template_name="users.html"),name='search'),
    path('searchusers/',searchUsers,name='searchusers'),

    path('viewprofile/',viewprofile,name='view profile'),
    path('updateprofile/',updateprofile,name='update profile'),
    path('updateresume/',updateresume,name='update resume'),

    path('download/',download,name='download'),

    path('addquestion/',TemplateView.as_view(template_name = 'addquestion.html'),name='question'),
    path('questionaction/',addQuestion,name='question action'),
    path('getquestions/',getquestions,name='questions'),
    path('deletequestion/',deletequestion,name='deletequestion'),

    path('answerquestion/',answerquestion,name='deletequestion'),
    path('answerquestionaction/',answerquestionaction,name='deletequestion'),
    path('sendemail/',sendemail,name='deletequestion'),


    path('logout/',logout,name='logout'),
]

from django.contrib import admin

from resume.models import UserModel,QuestionModel,AnswerModel

admin.site.register(UserModel)
admin.site.register(QuestionModel)
admin.site.register(AnswerModel)

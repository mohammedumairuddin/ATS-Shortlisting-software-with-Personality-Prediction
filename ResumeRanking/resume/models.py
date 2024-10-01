from django.db import models

from django.db.models import Model

class UserModel(Model):

    email = models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    age=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    name=models.CharField(max_length=50,default="")
    mobile=models.CharField(max_length=50,default="")
    resume = models.FileField(upload_to="documents")

class QuestionModel(models.Model):
    question = models.CharField(max_length=60)
    type = models.CharField(max_length=60)

class AnswerModel(models.Model):
    questionid = models.CharField(max_length=60)
    studentid= models.CharField(max_length=60)
    score=models.CharField(max_length=60)
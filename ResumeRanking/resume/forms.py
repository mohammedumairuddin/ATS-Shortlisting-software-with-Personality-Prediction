from django.forms import Form, CharField, PasswordInput, FileField

class UserForm(Form):

    email = CharField(max_length=50)
    password = CharField(max_length=50)
    name = CharField(max_length=50)
    mobile = CharField(max_length=50)
    gender = CharField(max_length=50)
    age = CharField(max_length=50)
    resume = FileField()

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class UpdateResumeForm(Form):
    resume = FileField()

class UpdateProfileForm(Form):
    password = CharField(max_length=50)
    mobile = CharField(max_length=50)
    age = CharField(max_length=30000)

class QuestionForm(Form):
    question = CharField(max_length=30000)
    type = CharField(max_length=30000)
    
class AnswerForm(Form):
    postid = CharField(max_length=30000)
    studentid= CharField(max_length=30000)
    openness=CharField(max_length=30000)
    neuroticism=CharField(max_length=30000)
    conscientiousness=CharField(max_length=30000)
    agreeableness=CharField(max_length=30000)
    extraversion=CharField(max_length=30000)
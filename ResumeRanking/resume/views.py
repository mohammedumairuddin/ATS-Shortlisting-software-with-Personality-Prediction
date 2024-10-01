from django.http import FileResponse
from django.shortcuts import render

from resume import constants
from resume.forms import UserForm, LoginForm, UpdateResumeForm, UpdateProfileForm, QuestionForm
from resume.models import UserModel, QuestionModel, AnswerModel
import numpy as np
import PyPDF2

from resume.constants import model_path
import smtplib

from sklearn.preprocessing import StandardScaler
import joblib
model = joblib.load(model_path+"/train_model.pkl")
scaler = StandardScaler()

def registration(request):

    if request.method == "POST":

        userForm = UserForm(request.POST,request.FILES)

        if userForm.is_valid():

            userModel = UserModel()

            userModel.email = userForm.cleaned_data["email"]
            userModel.password = userForm.cleaned_data["password"]
            userModel.name = userForm.cleaned_data["name"]
            userModel.mobile = userForm.cleaned_data["mobile"]
            userModel.resume=userForm.cleaned_data["resume"]
            userModel.gender = userForm.cleaned_data["gender"]
            userModel.agee = userForm.cleaned_data["age"]


            user = UserModel.objects.filter(email=userModel.email).first()

            if user is not None:
               return render(request, 'registration.html', {"message": "User All Ready Exist"})

            else:
                userModel.save()
                return render(request, 'index.html',{"message": "Registered Successfully"})

        return render(request, 'registration.html', {"message": "Invalid Form"})

    return render(request, 'registration.html', {"message": "Invalid Request"})

def login(request):

    if request.method == "GET":

        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            if uname == "admin" and upass == "admin":

                request.session['username'] = "admin"
                request.session['role'] = "admin"

                return render(request, "users.html",locals())

            else:

                user = UserModel.objects.filter(email=uname, password=upass).first()

                if user is not None:
                    request.session['username'] = uname
                    request.session['role'] = "user"

                    user = UserModel.objects.get(email=request.session['username'])
                    user.resume = str(user.resume).split("/")[1]
                    return render(request, 'viewprofile.html',
                                  {"profile": user,"email":user.email})

                else:
                    return render(request, 'index.html', {"message": "Invalid username or Password"})

        return render(request, 'index.html', {"message": "Invalid Form"})

    return render(request, 'index.html', {"message": "Invalid Credentials"})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})

def viewprofile(request):
    user=UserModel.objects.get(email=request.session['username'])
    user.resume = str(user.resume).split("/")[1]
    return render(request, 'viewprofile.html',
                  {"profile": user,"email":user.email})

def updateprofile(request):

    if request.method == "POST":
        # Get the posted form
        updateProfileForm = UpdateProfileForm(request.POST)

        if updateProfileForm.is_valid():

            password = updateProfileForm.cleaned_data["password"]
            mobile = updateProfileForm.cleaned_data["mobile"]
            age = updateProfileForm.cleaned_data["age"]

            UserModel.objects.filter(email=request.session['username']).update(password=password,mobile=mobile,age=age)

    user = UserModel.objects.get(email=request.session['username'])
    user.resume = str(user.resume).split("/")[1]

    return render(request, 'viewprofile.html', {"profile":user})

def updateresume(request):

    if request.method == "POST":

        updateresumefrom = UpdateResumeForm(request.POST,request.FILES)

        if updateresumefrom.is_valid():

            user = UserModel.objects.filter(email=request.session['username']).first()
            user.resume = updateresumefrom.cleaned_data["resume"]

            UserModel.objects.filter(email=request.session['username']).delete()
            user.save()

        user = UserModel.objects.get(email=request.session['username'])
        user.resume = str(user.resume).split("/")[1]
        return render(request, 'viewprofile.html', {"profile": user,"email":user.email})

#==============================================================================

def searchUsers(request):

    #  Saving POST file to storage
    keywords = request.POST['keywords']
    keywordList=keywords.split(",")
    #==========================================================

    users = []

    for user in UserModel.objects.all():

        resume_path = constants.document_path + "\\" + str(user.resume)
        resume_content = ""
        with open(resume_path, 'rb') as pdf_file:
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            number_of_pages = read_pdf.getNumPages()
            for page_number in range(number_of_pages):  # use xrange in Py2
                page = read_pdf.getPage(page_number)
                page_content = page.extractText()
                resume_content = resume_content + page_content

        ismatched=False

        for keyword in keywordList:
            if keyword in resume_content:
                ismatched=True


        if ismatched:

            inputs = dict()
            types=['openness',"neuroticism","conscientiousness","agreeableness","extraversion"]

            for type in types:

                count=0
                score=0

                for question in QuestionModel.objects.filter(type=type):
                    answer=AnswerModel.objects.filter(studentid=user.email,questionid=question.id).first()
                    if answer is not None:
                        count = count + 1
                        score=score+int(answer.score)

                avg=0
                if count!=0 and score!=0:
                    avg=score/count

                inputs.update({type:avg})

            print("Input:",inputs)

            gender = user.gender

            if (gender == "female"):
                gender_no = 1
            else:
                gender_no = 2

            print("user age:",user.age)
            age = float(user.age)
            openness = inputs['openness']
            neuroticism = inputs['neuroticism']
            conscientiousness = inputs['conscientiousness']
            agreeableness = inputs['agreeableness']
            extraversion = inputs['extraversion']

            print("i1",openness)
            print("i2", neuroticism)
            print("i3",conscientiousness)
            print("i4", agreeableness)
            print("i5", extraversion)
            print("G", gender_no)
            print("A", age)

            result = np.array([gender_no, age, openness, neuroticism, conscientiousness, agreeableness, extraversion],ndmin=2)
            final = scaler.fit_transform(result)
            personality = str(model.predict(final)[0])

            user.personality=personality

            users.append(user)

    return render(request,"users.html",{"users":users})

#================================================================================

def download(request):
    user=UserModel.objects.filter(email=request.GET['email']).first()
    resume_path = constants.document_path+"\\"+str(user.resume)
    response = FileResponse(open(resume_path, 'rb'))
    return response

#=====================================================================================

def addQuestion(request):

    questionForm = QuestionForm(request.POST)

    if questionForm.is_valid():

        question = questionForm.cleaned_data['question']
        type = questionForm.cleaned_data['type']

        QuestionModel(question=question,type=type).save()

        return render(request, "viewquestions.html", {"message": "Questioned Successfully!", "questions":QuestionModel.objects.all()})

    else:
        return render(request, 'viewquestions.html', {"message": "in valid request"})

def getquestions(request):

    if request.session['role']=="user":

        questions=[]

        for question in QuestionModel.objects.all():
            answer = AnswerModel.objects.filter(studentid=request.session['username'], questionid=question.id).first()
            question.isanswered = "no"
            if answer is not None:
                question.isanswered = "yes"

            questions.append(question)

        return render(request, "viewquestions.html", {"questions":questions})

    else:
        return render(request, "viewquestions.html", {"questions": QuestionModel.objects.all()})

def deletequestion(request):

    question_id = request.GET['question']
    QuestionModel.objects.filter(id=question_id).delete()
    return render(request, "viewquestions.html", {"questions": QuestionModel.objects.all()})

def answerquestion(request):
    question=QuestionModel.objects.filter(id=request.GET['question']).first()
    return render(request, "answerquestion.html", {"question":question})


def sendemail(request):

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()

        s.login("sender_email_id", "sender_email_id_password")

        message = "Your Resume Selected"
        s.sendmail("sender_email_id", request.GET['email'], message)

        s.quit()
    except Exception as e:
        pass

    return render(request, "users.html", {})

def answerquestionaction(request):

    question_id = request.POST['id']
    score = request.POST['score']
    AnswerModel(questionid=question_id,studentid=request.session['username'],score=score).save()

    if request.session['role']=="user":

        questions=[]

        for question in QuestionModel.objects.all():
            answer = AnswerModel.objects.filter(studentid=request.session['username'], questionid=question.id).first()
            question.isanswered = "no"
            if answer is not None:
                question.isanswered = "yes"

            questions.append(question)

        return render(request, "viewquestions.html", {"questions":questions})

    else:
        return render(request, "viewquestions.html", {"questions": QuestionModel.objects.all()})
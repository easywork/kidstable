from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# from .models import QuestionGenerator, Question, ClassOneQuestion, ClassThreeQuestion
from .models import Question, QuestionFactory

# NUMBER_OF_QUESTIONS = 20

def questionHome(request):
	#return HttpResponse('This is the test page')
	return render(request, 'questionhome.html')

def questionHome2(request):
    return render(request, 'questionhome2.html')

def getQuestions(request):
    classtype = request.POST['classtype']
    numberOfQuestions = int(request.POST['number'])
    questionFactory = QuestionFactory(classtype)
    questions = questionFactory.getInstances(numberOfQuestions)
    return render(request, 'getquestions.html', {'questions':questions})

def getAnswers(request):
    querystr = request.POST 
    results = []
    for name in querystr:  # loop over the 'name' from query strings
        if name.startswith('csr'):
            continue
        question = Question(name)
        answer = question.getAnswer()
        result = str(question) + ' = ' + str(answer)
        results.append(result)
    return render(request, 'getanswers.html', {'results':results})

def getQuestions(request):
    classtype = request.POST['classtype']
    numberOfQuestions = int(request.POST['number'])
    questionFactory = QuestionFactory(classtype)
    questions = questionFactory.getInstances(numberOfQuestions)
    return render(request, 'getquestions.html', {'questions':questions})

def makeQuestions(request):
    return render(request, 'questionhome.html')


def saveQuestions(request):
    classtype = request.POST['classtype']
    numberOfQuestions = int(request.POST['number'])
    questionFactory = QuestionFactory(classtype)
    questions = questionFactory.getInstances(numberOfQuestions)
    return render(request, 'getquestions.html', {'questions':questions})
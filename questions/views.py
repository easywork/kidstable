from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
# from .models import QuestionGenerator, Question, ClassOneQuestion, ClassThreeQuestion
from .models import Question, QuestionFactory
from . import models
from . import dao
from . import services

# NUMBER_OF_QUESTIONS = 20

def questionHome(request):
	#return HttpResponse('This is the test page')
	return render(request, 'questionhome.html')

def getQuestions(request):
    classtype = request.POST['classtype']
    numberOfQuestions = int(request.POST['number'])
    questionFactory = QuestionFactory(classtype)
    questions = questionFactory.getInstances(numberOfQuestions)
    return render(request, 'getquestions.html', {'questions':questions})

def getQuestions2(request):
    seed = int(request.POST['seed'])
    operand = request.POST['operand']
    numberOfQuestions = int(request.POST['number'])
    questionFactory = QuestionFactory()
    questionCreator = models.XQuestionCreator(seed, operand)
    questionFactory.questionCreator = questionCreator
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
        result = str(question) + str(answer)
        results.append(result)
    return render(request, 'getanswers.html', {'results':results})

def verify(request):
    querystr = request.POST 
    questions_ = []
    answers_ = []
    for name in querystr:  # loop over the 'name' from query strings
        if name.startswith('csr'):
            continue
        question = name
        answer = request.POST[question]
        #print('question is {} answer is {}'.format(question_, answer))
        questions_.append(question)
        answers_.append(answer)
    results_ = services.verify(questions_, answers_)
    results = _warpQuestionsAndResults(questions_, answers_, results_)
    #parms = {'questions':questions_, 'answers':answers_, 'results':results}
    return render(request, 'verify.html', {'results':results})

def _warpQuestionsAndResults(questions, answers, results):
    X = []
    for i in range(0, len(questions)):
        entry = questions[i] + answers[i]
        X.append([entry, results[i]])
    return X

def getQuestions(request):
    classtype = request.POST['classtype']
    numberOfQuestions = int(request.POST['number'])
    questionFactory = QuestionFactory(classtype)
    questions = questionFactory.getInstances(numberOfQuestions)
    # questionInFormats = [ q.printf() for q in questions]
    return render(request, 'getquestions.html', {'questions':questions})

def makeQuestions(request):
    return render(request, 'questionhome.html')

def saveQuestions(request):
    querystr = request.POST 
    table = dict()
    dao_ = dao.SessionCacher()
    for name in querystr:  # loop over the 'name' from query strings
        if name.startswith('csr'):
            continue
        question_ = name
        answer = request.POST[question_]
        #print('question is {} answer is {}'.format(question_, answer))
        table[question_] = answer
    session_id = dao_.save(table)
    return render(request, 'returnsessionid.html', {'session_id':session_id})

def retrieveQuestionBySessionId(request):
    session_id = request.POST['sessionid']
    dao_ = dao.SessionCacher()
    questionlist = dao_.retrieve(session_id)
    return render(request, 'retrievesession.html', {'questionlist':questionlist})





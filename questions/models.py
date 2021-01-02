
from django.db import models
import random

class Question(object):
	@staticmethod
	def getOperand(operands):
		return random.choice(operands)

	def __init__(self, question_=''):
		self.numbers = []
		self.operands = []
		if question_.endswith('='):
			question_ = question_[:-1]
		self.question = question_
		self.answer = ''
		if self.question != '':
			self.parse()
		# TODO self validate and raise error if it is invalid

	def parse(self):
		pass		

	def validate(self):
		o1 = self.operands[0]
		if o1 == '-' and self.numbers[1] > self.numbers[0]:
			return False
		else:
			return True
	
	def getAnswer(self):
		if self.answer != '':
			return self.answer
		else:
			answer = self._compute() 
			return answer

	def _compute(self):
		x = compile(self.question,'','eval')
		result = eval(x)
		return result

	def __eq__(self, other):
		if self.__str__() == other.__str__():
			return True
		else:
			return False

	def __str__(self):
		if self.question != '':
			return self.question
		else:
			return self._constructQuestion()

	def _constructQuestion(self):
		str_ = ''
		i = 0
		while i < len(self.numbers) and i < len(self.operands):
			str_ = str_ + str(self.numbers[i]) + self.operands[i]
			i += 1
		for t in range(i,len(self.numbers)):
			str_ = str_ + str(self.numbers[t]) 
		for t in range(i,len(self.operands)):
			str_ = str_ + self.operands[t]
		str_ = str_ + '='
		self.question = str_
		return str_

class QuestionCreator():
	def __init__(self):
		self.question = Question()

	def getInstance(self):
		pass

class ClassOneQuestion(Question):
	OPERAND_RANGE = '+-'  # static variable for classOneQuestion

	def parse(self):
		try:
			number = ''	
			for i in self.question:
				if i not in self.OPERAND_RANGE:
					number = number + i
				else:
					self.operands.append(i)
					self.numbers.append(int(number))
					number = ''
			self.numbers.append(int(number)) # add in the last number
		except ValueError:
			raise ValueError(i + " is not a valid operand")
			# '=' should also be raised as an error
			# TODO create test DB 
			# TODO '1^2' is not failing,  as 1^2 will go into one number but never get int() operate

class ClassOneQuestionCreator(QuestionCreator):
	def getInstance(self):
		self.question = ClassOneQuestion()
		while True:
			_numbers = []
			_operands = []
			x = random.randint(10,30)
			y = random.randint(5,20)
			_numbers.append(x), _numbers.append(y)
			o1 = Question.getOperand(ClassOneQuestion.OPERAND_RANGE)
			_operands.append(o1)
			self.question.numbers = _numbers
			self.question.operands = _operands
			if self.question.validate():
				break
		return self.question
			
class ClassThreeQuestion(Question):
	OPERAND_RANGE = '+-%/'  # static variable for classOneQuestion

class ClassThreeQuestionCreator(QuestionCreator):
	def getInstance(self):
		self.question = ClassThreeQuestion()
		x = random.randint(0,100)
		y = random.randint(0,100)
		self.question.numbers.append(x)
		self.question.numbers.append(y)
		o1 = Question.getOperand(ClassThreeQuestion.OPERAND_RANGE)
		self.question.operands.append(o1)
		return self.question

'''
 We use the Questions class to encapsulate the internal use of list to hold the question instances. This allows better encaplusation 
 for future change.  See <<clean code>>  P115 
'''
class QuestionFactory(object):
	def __init__(self, questiontype):
		self.questionCreator = QuestionCreator()
		if questiontype == 'Class One':
			self.questionCreator = ClassOneQuestionCreator()
		if questiontype == 'Class Three':		
			self.questionCreator = ClassThreeQuestionCreator()

	def getInstances(self, numberOfQuestions):
		questions = []
		for _ in range(0, numberOfQuestions):
			q = self.questionCreator.getInstance()
			questions.append(q)
		return questions

'''
Workflow of using Django Forms:
* add model using django model
* setting.py > Intall_APPS,  add 'questions'
* add the new model to admin.py
* Every time makes change to a model, need to apply the migration CLI
# manage.py makemigrations
# python mpython manage.py migrate
# python mpython manage.py createsuperuser
'''

class QuestionDao(models.Model):
	question = models.CharField(max_length = 50)
	# question = models.TextField()  # textField doesn't control length
	session = models.CharField(max_length = 50)
	answer = models.CharField(max_length = 50)
	
	def saveQuestion(self, question_):
		self.question = question_.question
		self.answer = question_.compute()
		self.session = 0
		self.save()

	def retrieve(self):
		questions = QuestionDao.objects.all()
		return questions

	class Meta:
		db_table = "questions"

'''
[ Note ]

 _method can be overriden in subclass,  but __method cannot
 static method can never but also never need to be overriden

References for implementing calculator in python
https://levelup.gitconnected.com/3-ways-to-write-a-calculator-in-python-61642f2e4a9a

'''

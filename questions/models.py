
from django.db import models
import random

CLASS_ONE = 'First Class'
CLASS_TWO = 'Second Class'
CLASS_THREE = 'Third Class'
CLASS_FOUR = 'Forth Class'
CLASS_FIVE = 'Fifth Class'
CLASS_SIX = 'Sixth Class'

CLASS_TYPES = (
	(CLASS_ONE, 1),
	(CLASS_TWO, 2),
	(CLASS_THREE, 3),
	(CLASS_FOUR, 4),
	(CLASS_FIVE, 5),
	(CLASS_SIX, 6)
)

class Question(object):
	OPERAND_RANGE = '+-*/()'  

	def __init__(self, question_=''):
		self.numbers = []
		self.operands = []
		self.classType = CLASS_ONE
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
	
	# def format(self):
	# 	out = self.question
	# 	if out.contains('*'):
	# 		out.replace('*', '')
	# 	f = self.question + '='
	# 	return f

	def __eq__(self, other):
		if self.__str__() == other.__str__():
			return True
		else:
			return False

	def __str__(self):
		if self.question != '':
			return self.question + '='
		else:
			self._constructQuestion()
			return self.question + '='

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
		str_ = str_ 
		self.question = str_ 
		return str_

class QuestionCreator():
	def __init__(self):
		self.question = Question()

	def getInstance(self):
		pass

	def getOperand(self):
		operands = self.question.OPERAND_RANGE
		return random.choice(operands)

class ClassOneQuestion(Question):
	OPERAND_RANGE = '+-'  # static variable for classOneQuestion
	
	def __init__(self, question_=''):
		super(ClassOneQuestion, self).__init__(question_)
		self.classType = CLASS_ONE

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

class ClassOneQuestionCreator(QuestionCreator):
	def getInstance(self):
		self.question = ClassOneQuestion()
		while True:
			_numbers = []
			_operands = []
			x = random.randint(10,30)
			y = random.randint(5,20)
			_numbers.append(x), _numbers.append(y)
			o1 = self.getOperand()
			_operands.append(o1)
			self.question.numbers = _numbers
			self.question.operands = _operands
			if self.question.validate():
				break
		return self.question
			
class ClassThreeQuestion(Question):
	OPERAND_RANGE = '+-%/'  # static variable for classOneQuestion

	def __init__(self, question_=''):
		super(ClassThreeQuestion, self).__init__(question_)
		self.classType = CLASS_THREE

class ClassThreeQuestionCreator(QuestionCreator):
	QUESTION_SKELETON1 = 'x+y+z'
	QUESTION_SKELETON2 = 'x+y-z'
	QUESTION_SKELETON3 = 'x-y+z'
	QUESTION_SKELETON4 = 'x-y-z'
	QUESTION_SKELETON5 = 'x*y'
	QUESTION_SKELETON6 = 'x/y'
	QUESTION_SKELETONS = [QUESTION_SKELETON1, QUESTION_SKELETON2, QUESTION_SKELETON3,
		QUESTION_SKELETON4, QUESTION_SKELETON5, QUESTION_SKELETON6]

	def getInstance(self):
		question_ = self. _getQuestionSkeleton()
		xyz = self._getXYZ()
		x = xyz[0]; y = xyz[1]; z = xyz[2]
		
		if question_ == self.QUESTION_SKELETON2:
			while x+y < z :
				xyz = self._getXYZ()
				x = xyz[0]; y = xyz[1]; z = xyz[2]
		if question_ == self.QUESTION_SKELETON3:
			while x < y:
				xyz = self._getXYZ()
				x = xyz[0]; y = xyz[1]; z = xyz[2]				
		if question_ == self.QUESTION_SKELETON4:
			while x < y or (x-y) < z:
				xyz = self._getXYZ()
				x = xyz[0]; y = xyz[1]; z = xyz[2]
		if question_ == self.QUESTION_SKELETON5:
			while x > 9 or y > 9:
				x = random.randint(2,9)
				y = random.randint(2,9)
		if question_ == self.QUESTION_SKELETON6:
			while x / y == 0 or x % y != 0:
				x = random.randint(4,81)
				y = random.randint(2,9)

		question_ = question_.replace('x',str(x))
		question_ = question_.replace('y',str(y))
		question_ = question_.replace('z',str(z))
		self.question = ClassThreeQuestion(question_)
		return self.question

	def _getQuestionSkeleton(self):
		t = random.randint(0,5)
		return self.QUESTION_SKELETONS[t]

	def _getXYZ(self):
		x = random.randint(10,100)
		y = random.randint(10,80)
		z = random.randint(10,50)
		return [x,y,z]

#  We use the Questions class to encapsulate the internal use of list to hold
#  the question instances. This allows better encaplusation for future change.  
# See <<clean code>>  P115 

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

class QuestionDao(models.Model):
	question = models.CharField(max_length = 80) # or use textField for unlimited length
	answer = models.CharField(max_length = 10)
	classType = models.CharField(max_length = 15, choices=CLASS_TYPES,default=CLASS_ONE)
	
	def saveQuestion(self, question_):
		self.question = question_.question
		self.answer = question_.compute()
		self.classType = question_.classType
		self.save()

	def retrieve(self):
		questions = QuestionDao.objects.all()
		return questions

	# reload the __str__ method in order to make it readable on admin page
	def __str__(self):
		return self.question

	class Meta:
		db_table = "questions"


# [ Note ]
#  _method can be overriden in subclass,  but _method cannot be
#  static method as whcih can never be overriden

# References for implementing calculator in python
# https://levelup.gitconnected.com/3-ways-to-write-a-calculator-in-python-61642f2e4a9a


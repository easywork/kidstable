from django.test import TestCase

# Create your tests here.
from .models import Question, ClassOneQuestion, ClassThreeQuestion, QuestionDao

class QuestionsTestcase(TestCase):

	def testClassOneQuestions(self):
		question1_ = '1+1'
		question1 = ClassOneQuestion(question1_)
		self.assertEqual(question1.question, question1_)
		with self.assertRaises(ValueError):
			question2_ = '1^2'
			question2 = ClassOneQuestion(question2_)

	def testGetAnswer(self):
		q1 = ClassOneQuestion('1+2')
		q2 = ClassThreeQuestion('5-4')
		q3 = Question('3*4')
		q4 = Question('5+3*(1+1)')
		self.assertEqual(q1.getAnswer(), 3)
		self.assertEqual(q2.getAnswer(), 1)
		self.assertEqual(q3.getAnswer(), 12)
		self.assertEqual(q4.getAnswer(), 11)

	# def testClassThreeQuestions(self):
	# 	questionText = '1+5-3=2'
	# 	question = ClassThreeQuestion()

	# def testCompute(self):
	# 	pass

	def testQuestionDao(self):
		# questions = QuestionDao.retrieve()
		q = QuestionDao()
		q.session = '001'
		q.answer = '0'
		q.question = '3+3'
		q.save()
		questions = q.retrieve()
		print('test retrieve')
		self.assertIn(questions[0].question, '3+3')
		# self.assertContains(response, "sth") # assertContains is for httpResponse


'''
if __name__ == '__main__()':
	testClassOneQuestions()

	testClassThreeQuestions()
'''
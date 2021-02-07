from django.test import TestCase

# Create your tests here.
from .models import Question, ClassOneQuestion, ClassThreeQuestion, ClassThreeQuestionCreator
from . import dao

class QuestionDaoTestcases(TestCase):

	def testQuestionDao(self):
		q = dao.QuestionDao()
		q.session = '001'
		q.answer = '0'
		q.question = '3+3'
		q.save()
		questions = q.retrieve()
		self.assertEqual(questions[0].question, '3+3')
		# self.assertContains(response, "sth") # assertContains is for httpResponse

	def testQuestionWithRedis(self):
		q1 = ClassOneQuestion('1+2')
		q2 = ClassThreeQuestion('5-4')
		q3 = Question('3*4')
		q4 = Question('5+3*(1+1)') 
		qset = {q1, q2, q3, q4}
		dao_ = dao.QuestionRedisDao()
		dao_.testMode()
		session_id = dao_.save(qset)
		assert session_id is not None
		print('the session id is {}'.format(session_id))
		qset2 = dao_.retrieve(session_id)
		print('The questions are {}'.format(qset2))
		self.assertIn(repr(q3), qset2)

	def testSessionCacher(self):
		q1 = ClassOneQuestion('1+2')
		q2 = ClassThreeQuestion('5-4')
		q3 = Question('3*4')
		q4 = Question('5+3*(1+1)')
		a1 = 1
		a2 = 2
		a3 = 0
		a4 = 4
		table = {repr(q1):a1, repr(q2):a2, repr(q3):a3, repr(q4):a4}
		dao_ = dao.SessionCacher()
		dao_.testMode(True)
		session_id = dao_.save(table)
		table_ = dao_.retrieve(session_id)
		# print(table_)
		self.assertEqual(table_[repr(q1)], str(a1))
		self.assertEqual(table_[repr(q3)], str(a3))
		print(table_)
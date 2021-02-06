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
		redis_db = dao.QuestionRedisDao()
		redis_db.testMode()
		session_id = redis_db.save(qset)
		assert session_id is not None
		print('the session id is {}'.format(session_id))
		qset2 = redis_db.get(session_id)
		print('The questions are {}'.format(qset2))
		self.assertIn(repr(q3).encode('utf8'), qset2)
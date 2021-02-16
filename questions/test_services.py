from django.test import TestCase

# Create your tests here.
from .models import Question, ClassOneQuestion, ClassThreeQuestion, ClassThreeQuestionCreator
from . import services

class ServiceTestcases(TestCase):
    def testVerifyService(self):
        q1 = '1+2'
        q2 = '5-4'
        q3 = '3*4'
        q4 = '5+3*(1+1)'
        a1 = Question(q1).getAnswer()
        a2 = Question(q2).getAnswer()
        a3 = Question(q3).getAnswer()
        a4 = 0
        questions = [q1, q2, q3, q4]
        answers = [a1, a2, a3, a4]
        results = services.verify(questions, answers)
        self.assertTrue(results[0])
        self.assertTrue(results[1])
        self.assertTrue(results[2])
        self.assertFalse(results[3])
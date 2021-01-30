from django.db import models
import json
from django.conf import settings # this refers to django's setting.py
import redis
import uuid
# from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework.response import Response

from . import models as questions

REDIS_PROD_DB = 0
REDIS_TEST_DB = 2

class QuestionDao(models.Model):
	question = models.CharField(max_length = 80) # or use textField for unlimited length
	answer = models.CharField(max_length = 10)
	classType = models.CharField(max_length = 15, choices=questions.CLASS_TYPES,default=questions.CLASS_ONE)
	
	def saveQuestion(self, question_):
		self.question = question_.repr()
		self.answer = question_.getAnswer()
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

class QuestionRedisDao(object):   
    redis_db = redis.StrictRedis(host=settings.REDIS_HOST,
                                port=settings.REDIS_PORT, db=REDIS_PROD_DB)

    def testMode(self, modeOn=True):
        if modeOn:
            redis_db = redis.StrictRedis(host=settings.REDIS_HOST,
                                        port=settings.REDIS_PORT, db=REDIS_TEST_DB)
        else:
            redis_db = redis.StrictRedis(host=settings.REDIS_HOST,
                                        port=settings.REDIS_PORT, db=REDIS_PROD_DB)

    def get(self, session_id):
        questions = self.redis_db.smembers(session_id)
        return questions

    def save(self, questions):
        session_id = uuid.uuid4().hex
        for q in questions:
            self.redis_db.sadd(session_id, repr(q))
        three_days = 3600 * 24
        self.redis_db.expire(session_id, three_days)
        return session_id 
        #TODO what if duplicate uuid ?

    #def remove(self, session_id):

# Some redis-cli
    # flush current DB: flushdb 
    # select <db number>
    # sadd <key> <set_member>, add member to set
    # smembers <kdey>, teturn a set by its key
    # del <key>


    

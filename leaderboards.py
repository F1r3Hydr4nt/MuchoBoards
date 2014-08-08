import cgi
import urllib

from google.appengine.ext import ndb
from model import *
import webapp2
import os
import ranker as ranker
import hashlib

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

APP_KEY = 'default'
MIN_SCORE = 0
MAX_SCORE = 999999
BRANCHING_FACTOR = 100
DEFAULT_NICKNAME = 'nickname'
DEFAULT_EMAIL = 'email'
DEFAULT_LEVEL = '0'
DEFAULT_SCORE = '555'
PRIVATE_KEY = '6Mot6YicAhtPVA2v7xAa'

isDebug = True
def debug(msg):
    if isDebug:
        print(msg)

def get_ranker(key):
    return ranker.Ranker.get_or_create(key, [MIN_SCORE, MAX_SCORE + 1], BRANCHING_FACTOR)
"""
Ranker has methods to set_score
r.set_score(name, [score]) (automatically ensures score is higher, so for time do opposite) ->
    r.get_score(name) if < etc.
score = int(self.request.get("score"))
r.find_rank([score])
r.find_score(rank) (Use this to get top ten and names)
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class CreateUser(webapp2.RequestHandler):
    def post(self):
        nickname = self.request.get('nickname', DEFAULT_NICKNAME)
        email = self.request.get('email', DEFAULT_EMAIL)
        hash_recieved = str(self.request.get('hash'))
        hash_ok = hash_okay([nickname, email,PRIVATE_KEY], hash_recieved)
        new_user_key = User.my_get_or_insert(nickname,user_id=nickname,email_address=email)
        if new_user_key[1] is False or hash_ok is False:
            # fail
            self.response.status = 403
            return
        else:
            self.response.status = 200
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write('{"result":"success"}')
            return

def hash_okay(strings, hash_received):
  str_to_hash = "".join(strings)+PRIVATE_KEY
  expected = hashlib.md5(str_to_hash).hexdigest()
  debug("Expected hash: " + expected)
  if (hash_received == expected):
    return True;
  else:
    return False;

class PostScore(webapp2.RequestHandler):
    def post(self):
        nickname = self.request.get('nickname', DEFAULT_NICKNAME)
        level_number = self.request.get('level_number', DEFAULT_LEVEL)
        level_score = self.request.get('score', DEFAULT_SCORE)
        level_time = self.request.get('time', DEFAULT_LEVEL)

        score_ranker_key='level_'+str(level_number)+'_score'
        score_ranker=get_ranker(score_ranker_key)
        score_ranker.set_score(nickname,[int(level_score)])

        user_rank = score_ranker.find_rank([int(level_score)])+1#zero_based ranking system +1st
        print user_rank

        #top_ten_scores = score_ranker.get_top_ten()
        #print(top_ten_scores)
        """
        q = datastore.Query('Scores')
        q['score <='] = rank.FindScore(1000)[0]
        next_twenty_scores = q.Get(20)
        """
        for x in range(0, 10):
            debug(score_ranker.FindScoreApproximate(x))
            debug(score_ranker.find_score(x))
            print(x)

        top_ten_scores = score_ranker.get_top_ten()
        print(top_ten_scores)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createUser', CreateUser),
    ('/postScore', PostScore),
], debug=True)


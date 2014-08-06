import cgi
import urllib

from google.appengine.ext import ndb
from model import *
import webapp2

DEFAULT_NICKNAME = 'nickname'
DEFAULT_EMAIL = 'email'
DEFAULT_LEVEL = '0'

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class CreateUser(webapp2.RequestHandler):
    def post(self):
        nickname = self.request.get('nickname', DEFAULT_NICKNAME)
        email = self.request.get('email', DEFAULT_EMAIL)
        new_user_key = User.my_get_or_insert(nickname,user_id=nickname,email_address=email)
        if new_user_key[1] is False:
            # fail
            self.response.status = 403
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write('{"result":"username taken"}')
            return
        else:
            self.response.status = 200
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write('{"result":"success"}')
            return

class PostScores(webapp2.RequestHandler):
    def post(self):
        nickname = self.request.get('nickname', DEFAULT_NICKNAME)
        level_number = self.request.get('level_number', DEFAULT_LEVEL)
        new_level = Level.my_get_or_insert(level_number,level_id=level_number)
        if new_level[1] is False:#create the level then
            new_level_key=new_level[0].put()
        level_score = self.request.get('score', DEFAULT_LEVEL)
        level_time = self.request.get('time', DEFAULT_LEVEL)
        level_score_entry_key = LevelScoreEntry.my_get_or_insert(nickname,parent=new_level_key)
        if level_score_entry_key[1] is False:
            entry_key = level_score_entry_key[0].put();
        else:
            entry_key=level_score_entry_key[0]
        score_entry = entry_key.get()
        if score_entry.best_score==None:
            score_entry.best_score=level_score
        if score_entry.best_time==None:
            score_entry.best_time=level_time
        score_entry.put()




application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createUser', CreateUser),
    ('/postResults', PostScores),
], debug=True)


from config import *
from post_score import PostScore

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


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createUser', CreateUser),
    ('/postScore', PostScore),
], debug=True)


import cgi
import urllib
import config
from google.appengine.ext import ndb
from model import *
import hashlib
import json

import os
import webapp2

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

import ranker as ranker
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
def hash_okay(strings, hash_received):
  str_to_hash = "".join(strings)+PRIVATE_KEY
  expected = hashlib.md5(str_to_hash).hexdigest()
  debug("Expected hash: " + expected)
  if (hash_received == expected):
    return True;
  else:
    return False;



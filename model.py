import cgi
import urllib

from google.appengine.ext import ndb

import webapp2

class User(ndb.Model):
    """Models an individual user best times."""
    user_id = ndb.StringProperty(required=True)#nickname
    email_address = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    @ndb.transactional
    def my_get_or_insert(cls, id, **kwds):
        key = ndb.Key(cls, id)
        ent = key.get()
        if ent is not None:
            return (ent, False)  # False meaning "not created"
        ent = cls(**kwds)
        ent.key = key
        ent.put()
        return (ent, True)  # True meaning "created"

class Level(ndb.Model):
    level_id = ndb.StringProperty(required=True)#level id

    @classmethod
    @ndb.transactional
    def my_get_or_insert(cls, id, **kwds):
        key = ndb.Key(cls, id)
        ent = key.get()
        if ent is not None:
            return (ent, False)  # False meaning "not created"
        ent = cls(**kwds)
        ent.key = key
        ent.put()
        return (ent, True)  # True meaning "created"

class LevelScoreEntry(ndb.Model):
    best_score = ndb.StringProperty()
    best_time = ndb.StringProperty()
    @classmethod
    @ndb.transactional
    def my_get_or_insert(cls, id, **kwds):
        key = ndb.Key(cls, id)
        ent = key.get()
        if ent is not None:
            return (ent, False)  # False meaning "not created"
        ent = cls(**kwds)
        ent.key = key
        ent.put()
        return (ent, True)  # True meaning "created"




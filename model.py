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

class Ranker(ndb.Model):
    """
        key = ranking_name ( unique string )
    """
    score_range = ndb.IntegerProperty(indexed=False, repeated=True)
    branching_factor = ndb.IntegerProperty(indexed=False)

class RankerScore(ndb.Model):
    """
        key = player_id
    """
    value = ndb.IntegerProperty(indexed=False, repeated=True)
    player_id = ndb.StringProperty(required=True)

class Scores(ndb.Model):
    """
        key = player_id
    """
    value = ndb.IntegerProperty(repeated=True)
    player_id =  ndb.StringProperty(required=True)

class Times(ndb.Model):
    """
        key = player_id
    """
    value = ndb.IntegerProperty(repeated=True)
    player_id =  ndb.StringProperty(required=True)

class RankerNode(ndb.Model):
    """
        key = node_id
    """
    child_counts = ndb.IntegerProperty(indexed=False, repeated=True)



from config import *

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




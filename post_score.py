from config import *

"""only top local scores must be sent from unity
    this is to avoid reprogramming checks here
    specifically for the second Scores which
    get_or_inserts regardless"""

class PostScore(webapp2.RequestHandler):
    def post(self):
        nickname = self.request.get('nickname', DEFAULT_NICKNAME)
        level_number = self.request.get('level_number', DEFAULT_LEVEL)
        level_score = self.request.get('score', DEFAULT_SCORE)
        level_time = self.request.get('time', DEFAULT_LEVEL)

        score_ranker_key='level_'+str(level_number)+'_score'
        score_ranker=get_ranker(score_ranker_key)
        score_ranker.set_score(nickname,[int(level_score)],False)

        user_rank = score_ranker.find_rank([int(level_score)])+1#zero_based ranking system +1st
        top_ten_scores = score_ranker.get_top_ten()
        print("TOP_SCORES-")
        print(top_ten_scores)
        #print [MIN_SCORE, MAX_SCORE + 1]
        time_ranker_key='level_'+str(level_number)+'_time'
        time_ranker=get_ranker(time_ranker_key)
        """As set_score only works for greater values or else it retains itself
        we must simply find the score for the user and if it exists and lower
        delete it and reset the new score"""
        time_ranker.set_score(nickname,[int(level_time)],True)
        #time is inverse
        user_rank_inverse = score_ranker.find_rank([int(level_score)])#zero_based ranking system +1st
        total_ranked = score_ranker.total_ranked_player_num()
        user_rank=total_ranked-user_rank_inverse
        top_ten_times = score_ranker.get_top_ten_times()
        print("TOP_TIMES-")
        print(top_ten_times)

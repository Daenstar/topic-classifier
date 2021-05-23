import json
import collections
from nltk.util import ngrams


class DataAnalyser:
    def __init__(self, topics_file):
        self.topics = []
        self.learning_dict = {}
        with open(topics_file, "r", encoding="utf-8") as fin:
            self.learning_dict = json.load(fin)
            for topic in self.learning_dict.keys():
                self.topics.append(topic)



    def __is_keyword_found(self, topic_keyword, normalized_post ):
        if ('+' in topic_keyword):
            #ключевое слово - составное
            keyword_splitted = topic_keyword.split('+')
            keyword_bigram = (keyword_splitted[0], keyword_splitted[1])
            #create bigrams
            post_bigrams = list(ngrams(normalized_post, 2))
            #search keyword_bigram in post_bigrams
            if(keyword_bigram in post_bigrams):
                return True
        else:
            if (topic_keyword in normalized_post):
                return True
        return False


    def predict_topic(self, normalized_post):
        #for word in normalized_post:
        for topic_name in self.learning_dict.keys():
            need_to_check_topic = True
            for stop_keyword in self.learning_dict[topic_name]['stopwords']:
                #print( self.learning_dict[topic_name])
                if(self.__is_keyword_found(stop_keyword, normalized_post)):
                    #print('stop:'+stop_keyword)
                    need_to_check_topic = False
                    break
            if (need_to_check_topic == False):
                #goto next topic
                continue
            for keyword in self.learning_dict[topic_name]['keywords']:
                # print( self.learning_dict[topic_name])
                if (self.__is_keyword_found(keyword, normalized_post)):
                    #topic detected
                    return topic_name

        return 'Other'

    def predict_topic_all_posts(self, posts):
        for post in posts:
            topic = self.predict_topic(post["text"])
            # print(topic+":::"+str(post["text"]))
            post["topic"] = topic


    #Считает долю постов с определенной тематикой среди всех постов за указанный год
    #+популярность тематики (лайки+shared) в указанный год
    def get_year_common_stats(self, posts, year):
        #постов за год
        total = 0
        #TOTAL_LS = 0
        #total_LS = 0
        stats = collections.defaultdict(lambda: collections.defaultdict(int))
        for post in posts:

            if(str(year) in post['time']):
                #TOTAL_LS += post['likes'] + post['shares']
                total += 1
                stats[post['topic']]['count'] += 1
                #total_LS += post['likes'] + post['shares']
                stats[post['topic']]['LS'] += post['likes'] + post['shares']
        for topic in stats.keys():
            stats[topic]['percent'] = stats[topic]['count'] / total * 100
            stats[topic]['LS_percent'] = stats[topic]['LS'] / stats[topic]['count']
       # print(TOTAL_LS)
        return stats


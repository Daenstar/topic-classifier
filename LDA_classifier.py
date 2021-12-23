import os
import pathlib
import matplotlib.pyplot as plt
import gensim
from gensim import corpora
import pickle
import numpy as np
import random
from gensim.models import CoherenceModel
from gensim.models.wrappers import LdaMallet

class LDAClassifier:
    # def __init__(self, topics_file):
    #     self.topics = []
    #     self.learning_dict = {}
    #     with open(topics_file, "r", encoding="utf-8") as fin:
    #         self.learning_dict = json.load(fin)
    #         for topic in self.learning_dict.keys():
    #             self.topics.append(topic)

    @staticmethod
    def __compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=2):
        current_dir = pathlib.Path(__file__).parent.absolute()
        mallet_path = os.path.join(current_dir, 'mallet-2.0.6', 'bin','mallet.bat')
        os.environ['MALLET_HOME'] = os.path.join(current_dir, 'mallet-2.0.6')
        coherence_values = []
        model_list = []
        for num_topics in range(start, limit, step):
            model = gensim.models.wrappers.LdaMallet (mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())
        return model_list, coherence_values

    @staticmethod
    def show_optimal_topics_count(normal_posts,start,limit,step):
        text_data = []
        for post in normal_posts:
            text_data.append(post["text"])
        dictionary = corpora.Dictionary(text_data)
        corpus = [dictionary.doc2bow(text) for text in text_data]

        model_list, coherence_values = \
            LDAClassifier.__compute_coherence_values(dictionary,
                                                   corpus,
                                                   text_data,
                                                   limit=limit,
                                                   start=start,
                                                     step=step)

        x = range(start, limit, step)
        plt.plot(x, coherence_values)
        plt.xlabel("Num Topics")
        plt.ylabel("Coherence score")
        plt.legend(("coherence_values"), loc='best')
        plt.show()



    @staticmethod
    def run( normal_posts, translated_posts ,lda_predicted_fname, num_topics):
        text_data = []
        #create list with post["text"]
        for post in normal_posts:
            text_data.append(post["text"])
            # print(topic+":::"+str(post["text"]))
            #post["topic"] = topic
        #create dict: 0-word1, 1-word2,...,N-wordN
        dictionary = corpora.Dictionary(text_data)
        # for k,v in dictionary.items():
        #     print(k,v)
        #корпус, состоит из списков, каждый список - текст поста, представленный в виде набора пар: (word_id, count)
        corpus = [dictionary.doc2bow(text) for text in text_data]
        NUM_TOPICS = num_topics
        rnd = np.random.RandomState(5)
        #RUN LDA algorithm
        ldamodel = gensim.models.ldamodel.LdaModel (
            corpus, num_topics=NUM_TOPICS, id2word=dictionary,
            passes=10, random_state = rnd, update_every=1,
            alpha='asymmetric', eta='symmetric')

        #ldamodel.save('model3.gensim')
      #  ldamodel.load('model3.gensim')


        
        # lda_display = pyLDAvis.prepare(ldamodel, corpus, dictionary, sort_topics=False)
        # pyLDAvis.display(lda_display)

        #Print topics (set of keywords)
        topics = ldamodel.print_topics(num_words=4)
        for topic in topics:
            print(topic)

        #Save posts+predicted topics to file
        with open(lda_predicted_fname, "w",encoding="utf-8") as fout:
            #row_list - list of keyword for topic
            for i, row_list in enumerate(ldamodel[corpus]):
                if i > 600:
                    break
                if i%3 == 0:
                    #sorted_by_second = sorted(data, key=lambda tup: tup[1])
                    #ldamodel для каждого поста хранит список возможных тем
                    #отсортируем их, чтобы получить наиболее вероятную тему
                    sorted_rowlist_by_probability =  sorted(row_list, key=lambda tup: tup[1])

                    #sorted_rowlist_by_probability - отсортир список возможных тем
                    #sorted_rowlist_by_probability[0] - наиболее вероятная тема
                    #sorted_rowlist_by_probability[0][0] - id наиболее вероятной темы
                    fout.write(str(sorted_rowlist_by_probability[0][0]) + ":" +translated_posts[i]["text"].replace("\n", "") + "\n\n")



        import pyLDAvis
        import pyLDAvis.gensim_models as gensimvis
        res = gensimvis.prepare(ldamodel, corpus, dictionary)
        pyLDAvis.show(res)




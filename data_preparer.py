import sys, os, re, math
import json
import nltk
import time
import pathlib
import html
import urllib.request
import urllib.parse
import pymorphy2
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('averaged_perceptron_tagger_ru')
# nltk.download('stopwords')
# nltk.download('wordnet')

agent = {'User-Agent':
         "Mozilla/4.0 (\
compatible;\
MSIE 6.0;\
Windows NT 5.1;\
SV1;\
.NET CLR 1.1.4322;\
.NET CLR 2.0.50727;\
.NET CLR 3.0.04506.30\
)"}


def unescape(text):
    if (sys.version_info[0] < 3):
        parser = HTMLParser.HTMLParser()
    else:
        parser = html
    return (parser.unescape(text))


def translate(to_translate, to_language="auto", from_language="auto"):
    base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"
    if (sys.version_info[0] < 3):#for Python 2.7
        to_translate = urllib.quote_plus(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        request = urllib2.Request(link, headers=agent)
        raw_data = urllib2.urlopen(request).read()
    else:#for Python 3.X
        to_translate = urllib.parse.quote(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        request = urllib.request.Request(link, headers=agent)
        raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = unescape(re_result[0])
    return (result)


class DataPreparer:
    def __init__(self, dest_lang):
        if (dest_lang not in ['en', 'ru']):
            raise Exception(f"Language {dest_lang} is not suppoted. "
                            f"Supported destination langs: en, ru")
        self.dest_lang = dest_lang
        self.posts = []
        self.posts_loaded = False

    def load_posts(self, jsonFilePath):
        self.posts = []
        with open(jsonFilePath, "r") as fin:
            for line in fin:
                post = json.loads(line)
                self.posts.append(post)
        self.posts_loaded = True

    def translate_posts(self):
        if(self.posts_loaded):
            for post in self.posts:

                translated = translate(post["text"], self.dest_lang, 'et')
                post["text"] = translated
                print(translated)
                time.sleep(1)



    def filter_words(self, for_LDA):
        #Регулярное выражения для удаления эмодзи и подобных символов
        emoji_removing_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U0001F1F2-\U0001F1F4"  # Macau flag
                                   u"\U0001F1E6-\U0001F1FF"  # flags
                                   u"\U0001F600-\U0001F64F"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U0001F1F2"
                                   u"\U0001F1F4"
                                   u"\U0001F620"
                                   u"\u200d"
                                   u"\u2640-\u2642"
                                   "]+", flags=re.UNICODE)


        for post in self.posts:
            pos_tag_lang = None
            post_without_emojies = emoji_removing_pattern.sub(r'', post["text"])

            #word_tokenize - разбивает предложение на отдельные слова (убирает пробелы, прочие знаки препинание) и помещает их в список
            words = nltk.word_tokenize(post_without_emojies)
            #print(words)
            #Части речи которые будут удалены из списка words
            if self.dest_lang == 'ru':
                pos_tag_lang = 'rus'
                part_of_speech_toremove = {'ADV', 'A-PRO','A-PRO=m',
                                           'A-PRO=n','ADV-PRO','A-PRO=pl',
                                           'CONJ', 'INTJ','NONLEX',
                                           'PART', 'PR', 'PRAEDIC-PRO',
                                          'PRAEDIC','PARENTH', 'S-PRO'
                                          }
                if for_LDA:
                    part_of_speech_toremove.add('NUM=ciph')

            elif self.dest_lang == 'en':
                pos_tag_lang = 'eng'
                part_of_speech_toremove = {'CC', 'DT', 'EX', 'IN', 'LS',
                                           'MD', 'PDT', 'PRP', 'RB', 'RBR', 'RBS',
                                           'RP', 'TO', 'UH','WDT','WP'}
                if for_LDA:
                    part_of_speech_toremove.add('CD')
            else:
                raise Exception(f"Language {self.dest_lang} is not suppoted. "
                                f"Supported destination langs: en, ru")

            post["text"] = [word for word, pos in nltk.pos_tag(words, lang=pos_tag_lang)
                            if pos not in part_of_speech_toremove]

            #for word, pos nltk.pos_tag(words, lang='rus') - сопоставить всем словам из списка words их части речи. Результат - набор пар: (слово:часть речи)
            #if pos not in part_of_speech_toremove - останутся только те пары (слово:часть_речи), часть_речи у которых не находится в списке part_of_speech_toremove
            #word - остаются только слова нужных частей речи и помещаются в список  post["text"]
            # for word, pos in nltk.pos_tag(words, lang='eng'):
            #     print (word + ":" +pos)


    def normalize_words(self, for_LDA):
        #Создание объекта MorphAnalyzer
        stop_words = []
        morph = pymorphy2.MorphAnalyzer()
        current_dir = pathlib.Path(__file__).parent.absolute()
        if self.dest_lang == 'ru':
            if for_LDA:
                with open(os.path.join(current_dir, "stop_words", "rus.txt"), 'r',encoding="utf-8") as fin:
                    stop_words = fin.read().splitlines()
            else:
                stop_words = stopwords.words('russian')
        elif self.dest_lang == 'en':
            with open(os.path.join(current_dir,"stop_words","eng.txt"),'r',encoding="utf-8") as fin:
                stop_words = fin.read().splitlines()
            #stop_words = stopwords.words('english')
            stop_words += list('.,;:#$%!?%@&*"`\'-·+=)([]}{|')
            stop_words += [ '\'s','``','\'\'','vkg','--','al','la','\'m','tee']
        # for e in stop_words:
        #     print (e)
        for post in self.posts:
            normalized_post = []
            for word in post["text"]:
                word = word.lower()
                word_normal = ""
                if self.dest_lang == 'ru':
                    #получить информацию о слове word (все возможные разборы слова)
                    #[0] - взятие наиболее вероятного разбора
                    p = morph.parse(word)[0]
                    #взятие нормальной формы
                    word_normal = p.normal_form
                elif self.dest_lang == 'en':
                    lemmatizer = WordNetLemmatizer()
                    word_normal = lemmatizer.lemmatize(word)
                if word_normal.lower() not in stop_words:
                    if self.dest_lang == 'en':
                        if not bool(re.search('[а-яА-Я]', word_normal))  \
                                and not bool(re.search(r'//*.*/', word_normal)) \
                                and not 'www.' in word_normal \
                                and not '.ee' in word_normal \
                                and not '.com' in word_normal \
                                and not any(i.isdigit() for i in word_normal):
                                #Добавление нормальной формы слова в пост
                            normalized_post.append(word_normal)
                    else:
                        normalized_post.append(word_normal)
                #print(nltk.pos_tag(words, lang='rus'))
            post["text"] = normalized_post
            print(normalized_post)


    def save_posts(self, jsonFilePath):
        with open(jsonFilePath, "w") as fout:
            for post in self.posts:
                json.dump(post, fout)
                fout.write("\n")

    @staticmethod
    def __compute_tf(word_dict, l):
        tf = {}
        sum_nk = len(l)
        for word, count in word_dict.items():
            tf[word] = count / sum_nk
        return tf

    @staticmethod
    def __compute_idf(strings_list):
        n = len(strings_list)
        idf = dict.fromkeys(strings_list[0].keys(), 0)
        for l in strings_list:
            for word, count in l.items():
                if count > 0:
                    idf[word] += 1

        for word, v in idf.items():
            idf[word] = math.log(n / float(v))
        return idf

    @staticmethod
    def __compute_tf_idf(tf, idf):
        tf_idf = dict.fromkeys(tf.keys(), 0)
        for word, v in tf.items():
            tf_idf[word] = v * idf[word]
        return tf_idf

    def tf_idf_demo(self):
        if (len(self.posts) < 3):
            raise Exception("Not enough posts. Minimum count=3")

        l_A = self.posts[0]["text"]
        l_B = self.posts[1]["text"]
        l_C = self.posts[2]["text"]
        word_set = set(l_A).union(set(l_B)).union(set(l_C))
        word_dict_A = dict.fromkeys(word_set, 0)
        word_dict_B = dict.fromkeys(word_set, 0)
        word_dict_C = dict.fromkeys(word_set, 0)
        for word in l_A:
            word_dict_A[word] += 1
        for word in l_B:
            word_dict_B[word] += 1
        for word in l_C:
            word_dict_C[word] += 1
        tf_A = self.__compute_tf(word_dict_A, l_A)
        tf_B = self.__compute_tf(word_dict_B, l_B)
        tf_C = self.__compute_tf(word_dict_C, l_C)
        idf = self.__compute_idf([word_dict_A, word_dict_B, word_dict_C])
        tf_idf_A = self.__compute_tf_idf(tf_A, idf)
        tf_idf_B = self.__compute_tf_idf(tf_B, idf)
        tf_idf_C = self.__compute_tf_idf(tf_C, idf)

        tf_idf_A = dict(sorted(tf_idf_A.items(), key=lambda item: item[1],reverse=True))
        tf_idf_B = dict(sorted(tf_idf_A.items(), key=lambda item: item[1],reverse=True))
        tf_idf_C = dict(sorted (tf_idf_A.items(), key=lambda item: item[1],reverse=True))

        i = 0
        for word, tfidf in tf_idf_A.items():
            if tfidf == 0:
                # if i > 20:
                #     break
                print (word,tfidf)
                i+=1
        # i = 0
        # for word, tfidf in tf_idf_B.items():
        #     if tfidf != 0:
        #         if i > 5:
        #             break
        #         print(word, tfidf)
        #         i += 1
        # i = 0
        # for word, tfidf in tf_idf_C.items():
        #     if tfidf != 0:
        #         if i > 5:
        #             break
        #         print(word, tfidf)
        #         i += 1\

    def rake_demo(self):
        # default
        if (len(self.posts) < 3):
            raise Exception("Not enough posts. Minimum count=3")
        r = Rake()

        # Extraction given the list of strings where each string is a sentence.
        r.extract_keywords_from_sentences([" ".join(self.posts[0]["text"]),
                                           " ".join(self.posts[2]["text"]),
                                           " ".join(self.posts[3]["text"])])

        print(r.get_ranked_phrases_with_scores())
#
#
#
# def translate(to_translate, to_language="auto", from_language="auto"):
#     #Формирование запроса
#     base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"
#     to_translate = urllib.parse.quote(to_translate)
#     link = base_link % (to_language, from_language, to_translate)
#     request = urllib.request.Request(link, headers=agent)
#     #Отправка запроса на сервер GoogleTranslate
#     raw_data = urllib.request.urlopen(request).read()
#     #Обработка ответа (извлечение переведенного текста)
#     data = raw_data.decode("utf-8")
#     expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
#     re_result = re.findall(expr, data)
#     if (len(re_result) == 0):
#         result = ""
#     else:
#         result = unescape(re_result[0])
#     return (result)
#
#
#
#

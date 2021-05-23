import sys, os, re
import json
import nltk
import time
import html
import urllib.request
import urllib.parse
import pymorphy2

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger_ru')

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
    def __init__(self):
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
                translated = translate(post["text"], 'ru', 'et')
                post["text"] = translated
                print(translated)
                time.sleep(1)


    def remove_unnecessary_words(self):
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
            post_without_emojies = emoji_removing_pattern.sub(r'', post["text"])
            #word_tokenize - разбивает предложение на отдельные слова (убирает пробелы, прочие знаки препинание) и помещает их в список
            words = nltk.word_tokenize(post_without_emojies)
            #Части речи которые будут удалены из списка words
            part_of_speech_toremove = {'ADV', 'CONJ','A-PRO', 'A-PRO=m','A-PRO=pl', 'S-PRO', 'PART', 'PR', 'NONLEX'}  # function words
            #for word, pos nltk.pos_tag(words, lang='rus') - сопоставить всем словам из списка words их части речи (выход - набор пар: слово:часть речи)
            #if pos not in part_of_speech_toremove - останутся только те пары слово:часть_речи, часть_речи у которых не находится в списке part_of_speech_toremove
            #word - остаются только слова нужных частей речи и помещаются в список  post["text"]
            post["text"] = [word for word, pos in nltk.pos_tag(words, lang='rus')
                            if pos not in part_of_speech_toremove]

    def normalize_words(self):
        #Создание объекта MorphAnalyzer
        morph = pymorphy2.MorphAnalyzer()
        for post in self.posts:
            normalized_post = []
            for word in post["text"]:
                #получить информацию о слове word (все возможные разборы слова)
                #[0] - взятие наиболее вероятного разбора
                p = morph.parse(word)[0]
                #взятие нормальной формы
                word_normal = p.normal_form
                #Добавление нормальной формы слова в пост
                normalized_post.append(word_normal)
                #print(nltk.pos_tag(words, lang='rus'))
            post["text"] = normalized_post


    def save_posts(self, jsonFilePath):
        with open(jsonFilePath, "w") as fout:
            for post in self.posts:
                json.dump(post, fout)
                fout.write("\n")
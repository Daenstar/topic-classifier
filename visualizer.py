import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator




#total=> 30%
def plot_accuracy_LDA_RU_6():
    index = np.arange(4)
    data = {'Проверяющий-1': [86,55,32,48],
            'Проверяющий-2':  [80,45,24,40],
            'Проверяющий-3':  [91,49,41,39],
            }
    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')
    plt.axis([-1, 4, 0, 100])
    plt.title('Правильность определения тематики постов', fontsize=14)
    plt.xlabel('Тематика', fontsize=14, loc="right")
    plt.ylabel('Процент верно\n классифицированных постов', fontsize=14,labelpad=30)
    plt.xticks(index, ['Текущая учеба',
                       'Работа',
                       'Горючий сланец',
                       'Курсы/лагерь'],
               rotation=0,fontsize=14)
    plt.show()


def plot_accuracy_LDA_RU_7():
    index = np.arange(5)
    data = {'Проверяющий-1': [86,55,32,48,30],
            'Проверяющий-2':  [80,45,24,40,28],
            'Проверяющий-3':  [91,49,41,39,32],
            }

    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')
    plt.axis([-1, 5, 0, 100])
    plt.title('Правильность определения тематики постов', fontsize=14)
    plt.xlabel('Тематика', fontsize=14, loc="right")
    plt.ylabel('Процент верно\n классифицированных постов', fontsize=14, labelpad=30)
    plt.xticks(index, ['Текущая учеба',
                       'Работа',
                       'Горючий сланец',
                       'Курсы/тренинги',
                       'Школа/гимназия'],
               rotation=0,
               fontsize=14)
    plt.show()

# 76+ 124- 200 => 38%
# (0,  текущая_учеба 39+ 14-
# (1, текущая_учеба 7+ 20-
# (2, текущая_учеба 16+ 3-  /62+ 37-
# (3,  работа 2+ 12-
# (4,  горючий_сланец 4+ 11-
# (5,  курсы_тренинги  7+ 15-
# (6,  лагерь 1+ 48-
def plot_accuracy_LDA_RU_18():
    index = np.arange(6)
    data = {'Проверяющий-1': [95,66,23,0,18,46],
            'Проверяющий-2':  [90,61,20,0,15,40],
            'Проверяющий-3':  [91,69,19,0,13,45],
            }
    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')
    plt.axis([-1, 6, 0, 100])
    plt.title('Правильность определения тематики постов', fontsize=14)
    plt.xlabel('Тематика', fontsize=14, loc="right")
    plt.ylabel('Процент верно\n классифицированных постов', fontsize=14, rotation=70,labelpad=30)
    plt.xticks(index, ['Текущая учеба',
                       'Работа',
                       'Горючий сланец',
                       'Научный лагерь',
                       'Изучение языка',
                       'Наука и техника'
                       ],
               rotation=10,fontsize=14)
    plt.show()

# =>> total: 48%
# учеба всего 106: 84+  20-
# (1,  курсы_тренинги 24- 4+
# (4,  горючий_сланец 10- 4+
# (6,  лагерь 18- 1+
# (7,  работа 30- 4+

def plot_accuracy_LDA_RU_8():
    index = np.arange(5)
    data = {'Проверяющий-1': [79,11,28,14,5],
            'Проверяющий-2':  [71,10,30,15,6],
            'Проверяющий-3':  [72,16,20,20,8],
            }
    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')
    plt.axis([-1, 5, 0, 100])
    plt.title( 'Правильность определения тематики постов', fontsize=14)
    plt.xlabel('Тематика', fontsize=14, loc="right")
    plt.ylabel( 'Процент верно\n классифицированных постов', fontsize=14,rotation=70,labelpad=30
                )
    plt.xticks(index, ['Текущая учеба',
                       'Работа',
                       'Горючий сланец',
                       'Курсы/тренинги',
                       'Научный лагерь',
                      ],
               rotation=0,fontsize=14)
    plt.show()




def plot_accuracy_LDA_EN_6():
    index = np.arange(3)
    data = {'Проверяющий-1': [81,20,46],
            'Проверяющий-2':  [80,24,47],
            'Проверяющий-3':  [84,26,53],
            }
    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')
    plt.axis([-1, 3, 0, 100])
    plt.title( 'Правильность определения тематики постов', fontsize=14)
    plt.xlabel('Тематика', fontsize=14, loc="right")
    plt.ylabel( 'Процент верно\n классифицированных постов', fontsize=14,labelpad=30
                )
    plt.xticks(index, ['Текущая учеба',#2 4 5 9 t53 total 65
                       'Горючий сланец',#7 8 3 t22 totoal 47
                       'Курсы/тренинги/лагерь',# t18 total 32
                      ],
               rotation=0,fontsize=14)
    plt.show()



def plot_accuracy_LDA_EN_10():
    index = np.arange(5)
    data = {'Проверяющий-1': [81,20,46,56,35],
            'Проверяющий-2':  [80,24,47,50,30],
            'Проверяющий-3':  [84,26,53,51,41],
            }
    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')
    plt.axis([-1, 5, 0, 100])
    plt.title( 'Правильность определения тематики постов', fontsize=14)
    plt.xlabel('Тематика', fontsize=14, loc="right")
    plt.ylabel( 'Процент верно\n классифицированных постов', fontsize=14,rotation=70,labelpad=30
                )
    plt.xticks(index, ['Текущая учеба',#2 4 5 9 t53 total 65
                       'Работа',#0 8/40
                       'Горючий сланец',#7 8 3 t22 totoal 47
                       'Курсы/лагерь',# t18 total 32
                       'Наука и техника',#t6 totoal 17
                      ],
               rotation=0,fontsize=14)
    plt.show()



def plot_accuracy_dict_rules():
    index = np.arange(6)
    ###V1(original)
    # data = {'Inspector-1': [83, 88, 81, 93, 90, 93],
    #         'Inspector-2': [85, 90, 80, 95, 92, 94],
    #         'Inspector-3': [80, 82, 74, 85, 89, 85],
    #         }
    ###V2
    data = {'Проверяющий-1': [83,77,81,93,81,84],
            'Проверяющий-2':  [85,70,80,95,84,79],
            'Проверяющий-3': [80, 78, 74, 91, 89, 75],
            }
    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')
    plt.axis([-1, 6, 0, 100])
    plt.title('Правильность определения тематики постов', fontsize=14)
    plt.xlabel('Тематика', fontsize=14)
    plt.ylabel('Процент верно классифицированных постов', fontsize=14,labelpad=30)
    plt.xticks(index, ['Происшествия',
                         'Прием на работу/учебу',
                       'Наука и техника',
                         'Текущая учеба',
                       'Курсы/тренинги',
                          'Прочее'],
               fontsize=14,
               rotation=15)
    plt.show()


def plot_distribution(distrib_19, distrib_20):
    index = np.arange(6)
    data = {'2019': distrib_19,
            '2020':  distrib_20,
            }
    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')

    plt.axis([-1, 6, 0, 35])
    plt.title('Распределение тематик постов в 2019/2020', fontsize=14)
    plt.xlabel('Тематика', fontsize=14,loc="right")
    plt.ylabel('Процент постов с данной тематикой',  fontsize=14,labelpad=30)
    plt.xticks(index, [
                     'Текущая учеба',
                        'Происшествия' ,
                        'Прием на работу/учебу',
                        'Наука и техника',
                        'Курсы/тренинги',
                        'Прочее'
                         ],
               rotation=15,fontsize=14)

    plt.show()



def plot_user_acivity(activity_19, activity_20):
    index = np.arange(6)
    data = {'2019': activity_19,
            '2020':  activity_20,
            }
    df = pd.DataFrame(data)
    df.plot(kind='bar')

    plt.rcParams["figure.figsize"] = (15, 8)
    plt.axis([-1, 6, 0, 12])
    plt.title('Активность пользователей в 2019/2020', fontsize=14)
    plt.xlabel('Тематика', fontsize=14)
    plt.ylabel('Рейтинг тематики среди пользователей', fontsize=14,labelpad=30)
    plt.xticks(index, [
                        'Текущая учеба',
                        'Происшествия'  ,
                        'Прием на работу/учебу',
                        'Наука и техника',
                        'Курсы/тренинги',
                        'Прочее'
    ],
               rotation=15,fontsize=14)
    plt.show()

def plot_datetime_distribution():
    pass


def show_wordcloud_txt(text):
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def show_wordcloud_posts_by_year(posts, year):
    text = [" ".join(post["text"]) for post in posts if str(year) in post["time"]]
    text = " ".join(text)
    word_cloud = WordCloud().generate(text)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

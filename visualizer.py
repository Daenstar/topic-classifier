import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_accuracy():
    index = np.arange(6)
    data = {'Inspector-1': [83,88,81,93,90,93],
            'Inspector-2':  [85,90,80,95,92,94],
            }
    plt.rcParams["figure.figsize"] = (15, 8)
    df = pd.DataFrame(data)
    df.plot(kind='bar')


    plt.axis([-1, 6, 0, 100])
    plt.title('Точность определения тематики постов', fontsize=14)
    plt.xlabel('Тематика', fontsize=12)
    plt.ylabel('Процент верно классифицированных постов', fontsize=12)
    plt.xticks(index, ['Происшествия',
                         'Прием на работу/учебу',
                       'Наука и техника',
                         'Текущая учеба',
                       'Курсы/тренинги',
                          'Прочее'],
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
    plt.xlabel('Тематика', fontsize=12)
    plt.ylabel('Процент постов с данной тематикой', fontsize=12)
    plt.xticks(index, [
                     'Текущая учеба',
                        'Происшествия' ,
                        'Прием на работу/учебу',
                        'Наука и техника',
                        'Курсы/тренинги',
                        'Прочее'
                         ],
               rotation=15)

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
    plt.xlabel('Тематика', fontsize=12)
    plt.ylabel('Отношение активности к числу постов в тематике', fontsize=12)
    plt.xticks(index, [
                        'Текущая учеба',
                        'Происшествия'  ,
                        'Прием на работу/учебу',
                        'Наука и техника',
                        'Курсы/тренинги',
                        'Прочее'
    ],
               rotation=15)
    plt.show()

def plot_datetime_distribution():
    pass
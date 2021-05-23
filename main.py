import json
import pathlib
from facebook_scraper import get_posts
# from classify_en import *
# from classify_ru import *
from data_preparer import *
from data_analyser import *
from visualizer import *



# import nltk
# nltk.download('stopwords')

#Вывод аналитики за 2019 и 2020 год в тектовом виде
def show_stats(stats_2019, stats_2020):
    for topic in stats_2019.keys():
         print(topic+"-2019:"+"{:.2f}".format(stats_2019[topic]['percent']) +
              # ";LS:"+ str(stats_2019[topic]['LS'])+
               ";LS_percent:"+"{:.2f}".format(stats_2019[topic]['LS_percent']))

         print(topic+"-2020:"+"{:.2f}".format(stats_2020[topic]['percent']) +
              # ";LS:"+ str(stats_2020[topic]['LS'])+
               ";LS_percent:"+"{:.2f}".format(stats_2020[topic]['LS_percent'])+'\n')

#Извлекает посты со страницы FB (pages_count пролистываний) в файл out_file
def exract_posts(page_name, out_file, pages_count):
    with open(out_file, "w", errors="ignore") as out:
        posts = get_posts(page_name, pages_count)
        #Проход по постам и извлечение только необходимых полей у постов
        for p in posts:
            # ФОрмирование объекта JSON для последующего сохр в файл с имененм save_to
            data = {}
            data["post_id"] = p["post_id"]
            data["text"] = p["text"]
            data["likes"] = p["likes"]
            data["comments"] = p["comments"]
            data["shares"] = p["shares"]
            data["time"] = (p["time"]).strftime("%Y-%m-%d")
            #Запись в файл
            json.dump(data, out)
            # Переход на новую строку
            out.write("\n")


#Сохранит классифифицированные по тематикам посты в папку target_dir
def save_classified_posts(classified_data, transtated_data, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    output_files = {'Курсы/Тренинги/Мероприятия':'courses-trainings.txt','Other':'other.txt',
                    'Происшествия':'accidents.txt','Текущая учеба':'study.txt',
                    'Прием на учебу/работу':'join-work-study.txt','Наука и техника':'science-tech.txt'}

    i = 0
    for post in classified_data.posts:
        with open(os.path.join(target_dir, output_files[post["topic"]]),'a',encoding='utf-8') as out:
            out.write(post["topic"])
            out.write('\t\t\t')
            out.write(transtated_data.posts[i]['text'].replace("\n", ""))
            out.write('\n')
            out.write('\n')
        i += 1

if __name__ == '__main__':


    current_dir = pathlib.Path(__file__).parent.absolute()
    extracted_filename = os.path .join(current_dir, "posts", 'TalTechVK_out.json')
    translated_filename = os.path .join(current_dir, "posts", 'TalTechVK_out_translated.json')
    dictonary_filename = os.path.join(current_dir, "topics", 'topics.json')
    normalized_filename = os.path.join(current_dir, "posts", 'TalTechVK_out_normalized.json')

    #=======================================
    # Полный цикл (выгрузка-перевод-обработка)
    #exract_posts('TalTechVK', extracted_filename, 220)
    # data = DataPreparer()
    # data.load_posts(extracted_filename)
    # data.translate_posts()
    # data.remove_unnecessary_words()
    # data.normalize_words()
    # data.save_posts(normalized_filename)
    # =======================================

    # =======================================
    # Сокращенный цикл (чтение обработанных постов-запуск алгоритма классификации)
    data = DataPreparer()
    data.load_posts(normalized_filename)
    # =======================================

    data_analyser = DataAnalyser(dictonary_filename)
    data_analyser.predict_topic_all_posts(data.posts)
    # Получение статистики по годам
    stats_2019 = data_analyser.get_year_common_stats(data.posts, 2019)
    stats_2020 = data_analyser.get_year_common_stats(data.posts, 2020)

    # ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ
    distrib_2019 = [stats_2019[topic]['percent'] for topic in sorted(stats_2019.keys(), reverse=True) ]
    distrib_2020 = [stats_2020[topic]['percent'] for topic in sorted(stats_2020.keys(), reverse=True) ]
    activity_2019 = [stats_2019[topic]['LS_percent'] for topic in sorted(stats_2019.keys(), reverse=True)]
    activity_2020 = [stats_2020[topic]['LS_percent'] for topic in sorted(stats_2020.keys(), reverse=True)]
    plot_accuracy()
    plot_distribution(distrib_2019, distrib_2020)
    plot_user_acivity(activity_2019, activity_2020)


    #СОХРАНЕНИЕ ПЕРЕВЕДЕННЫХ ПОСТОВ
    # target_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'posts')
    # data_translated = DataPreparer()
    # data_translated.load_posts(translated_filename)
    # save_classified_posts(data,data_translated, target_dir)






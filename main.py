import json
import pathlib
from facebook_scraper import get_posts
# from classify_en import *
# from classify_ru import *
from data_preparer import *
from data_analyser import *
from visualizer import *
from LDA_classifier import *



# import nltk
#Вывод аналитики за 2019 и 2020 год в тектовом виде
def show_stats(stats_2019, stats_2020):
    for topic in stats_2019.keys():
         print(topic+"-2019:"+"{:.2f}%".format(stats_2019[topic]['percent']) +
              # ";LS:"+ str(stats_2019[topic]['LS'])+
               " LikeShares_coeff:"+"{:.2f}".format(stats_2019[topic]['LikeShares_coeff']))

         print(topic+"-2020:"+"{:.2f}%".format(stats_2020[topic]['percent']) +
              # ";LS:"+ str(stats_2020[topic]['LS'])+
               " LikeShares_coeff:"+"{:.2f}".format(stats_2020[topic]['LikeShares_coeff'])+'\n')

#Извлекает посты со страницы FB (pages_count пролистываний) в файл out_file
def exract_posts(page_name, out_file, pages_count):
    with open(out_file, "w", errors="ignore") as out:
       # posts = get_posts(page_name, pages_count)
        posts = get_posts(page_name, page_limit=pages_count)
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
    output_files = {'Курсы/Тренинги/Мероприятия':'courses-trainings.txt',
                    'Other':'other.txt',
                    'Происшествия':'accidents.txt',
                    'Текущая учеба':'study.txt',
                    'Прием на учебу/работу':'join-work-study.txt',
                    'Наука и техника':'science-tech.txt'}

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
    extracted_filename = os.path.join(current_dir, "posts", 'TalTechVK_out.json')
    extracted_filename_test = os.path .join(current_dir, "posts", 'TalTechVK_out_test.json')
    translated_filename_ru = os.path .join(current_dir, "posts", 'TalTechVK_out_translated_RU.json')
    translated_filename_ru_new = os.path .join(current_dir, "posts", 'TalTechVK_out_translated_RU_new.json')
    translated_filename_en = os.path .join(current_dir, "posts", 'TalTechVK_out_translated_EN.json')
    dictonary_filename = os.path.join(current_dir, "topics", 'topics.json')
    normalized_filename_ru = os.path.join(current_dir, "posts", 'TalTechVK_out_normalized_RU.json')
    normalized_filename_en = os.path.join(current_dir, "posts", 'TalTechVK_out_normalized_EN.json')
    normalized_filename_test = os.path.join(current_dir, "posts", 'TalTechVK_out_normalized_test.json')

    normalized_filename_LDA_ru = os.path.join(current_dir, "posts", 'TalTechVK_out_normalized_debug.json')
    normalized_small_filename_ru = os.path.join(current_dir, "posts", 'TalTechVK_out_normalized_small_RU.json')
    lda_predicted_fname_ru = os.path.join(current_dir, "posts", 'TalTech_out_lda_predicted_results_RU.txt')
    lda_predicted_fname_en = os.path.join(current_dir, "posts", 'TalTech_out_lda_predicted_results_EN.txt')



    ## Выгрузка постов скраппером
    #exract_posts('TalTechVK', extracted_filename_test, 3)

    #=======================================
    ## Подготовка данных для анализа (выгрузка-перевод-обработка-сохранение)
    data = DataPreparer(dest_lang="ru")
    #data = DataPreparer(dest_lang="en")
    #data.load_posts(extracted_filename_test)
    #data.translate_posts()
    #data.save_posts(translated_filename_ru_new)

    ######TESTS::::
    #data.load_posts(translated_filename_ru_new)
    ##data.filter_words(for_LDA=False)
    #data.normalize_words(for_LDA=False)

    data.load_posts(translated_filename_ru)

    #data.load_posts(translated_filename_en)
    data.filter_words(for_LDA=False)
    #data.filter_words(for_LDA=True)
    data.normalize_words(for_LDA=False)
    # data_analyser = DataAnalyser(dictonary_filename)
    # print(data_analyser.get_count_of_words(data.posts, tokenized=True))
    # exit()
    #data.normalize_words(for_LDA=True)
    data.save_posts(normalized_filename_ru)
    #data.save_posts(normalized_filename_en)
    # #=======================================



    ##Алгоритм LDA#
    ### Чтение обработанных постов-запуск алгоритма классификации)
    #data = DataPreparer(dest_lang="en")
    #data.load_posts(normalized_filename_en)
    #data = DataPreparer(dest_lang="ru")
    #data.load_posts(normalized_small_filename_ru)
    #data.load_posts(normalized_filename_ru)
    # for p in data.posts:
    #      print(p['text'])
    #=======================================
    #data_translated = DataPreparer(dest_lang="ru")
    #data_translated.load_posts(translated_filename_ru)
    #num_topics = 14

    #LDAClassifier.show_optimal_topics_count(data.posts, start=2, limit=22, step=2)
    #LDAClassifier.run(data.posts, data_translated.posts, lda_predicted_fname_ru,num_topics)
    #LDAClassifier.run(data.posts, data_translated.posts, lda_predicted_fname_en,num_topics)
    # ====END LDA==============================


    # =======================================
    ## Алгоритм на основе словаря и правил
    data = DataPreparer(dest_lang="ru")
    data.load_posts(normalized_filename_ru)
    data_analyser = DataAnalyser(dictonary_filename)
    data_analyser.predict_topic_all_posts(data.posts)
    # Получение статистики по годам
    # print(data_analyser.get_most_liked_posts(data_translated.posts, 2019))
    # print(data_analyser.get_most_liked_posts(data_translated.posts, 2020))
    #print(data_analyser.get_most_shared_posts(data_translated.posts, 2019))
    #print(data_analyser.get_most_shared_posts(data_translated.posts, 2020))
    stats_2019 = data_analyser.get_year_common_stats(data.posts, 2019)
    stats_2020 = data_analyser.get_year_common_stats(data.posts, 2020)
    # show_stats(stats_2019,stats_2020)



    # ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ
    distrib_2019 = [stats_2019[topic]['percent'] for topic in sorted(stats_2019.keys(), reverse=True) ]
    distrib_2020 = [stats_2020[topic]['percent'] for topic in sorted(stats_2020.keys(), reverse=True) ]
    activity_2019 = [stats_2019[topic]['LikeShares_coeff'] for topic in sorted(stats_2019.keys(), reverse=True)]
    activity_2020 = [stats_2020[topic]['LikeShares_coeff'] for topic in sorted(stats_2020.keys(), reverse=True)]
    #plot_accuracy_LDA_RU_6()
    #plot_accuracy_LDA_EN_6()
    #plot_accuracy_LDA_RU_7()
    #plot_accuracy_LDA_RU_8()
    #plot_accuracy_dict_rules()
    plot_distribution(distrib_2019, distrib_2020)
    plot_user_acivity(activity_2019, activity_2020)

    # posts_2019 = [" ".join(post["text"]) for post in data.posts if "2019" in post["time"]]
    # posts_2019 = " ".join(posts_2019)
    #show_wordcloud_posts_by_year( data.posts, 2019)
    #show_wordcloud_posts_by_year (data.posts, 2020)
    # show_wordcloud_txt(posts_2019)
    # posts_2020 = [" ".join(post["text"]) for post in data.posts if "2020" in post["time"]]
    # posts_2020 = " ".join(posts_2020)
    # show_wordcloud(posts_2020)


    #СОХРАНЕНИЕ ПЕРЕВЕДЕННЫХ ПОСТОВ
    # target_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'posts')
    # data_translated = DataPreparer()
    # data_translated.load_posts(translated_filename)
    # save_classified_posts(data,data_translated, target_dir)






import csv
from database_connection.helpers.collections import question_bank, topics


def upload_question_bank():
    reader = csv.DictReader(open("question_bank.csv", encoding='utf-8-sig'))
    for raw in reader:
        keywords_list = []
        options_list = []
        for kv in raw['keywords'].split(","):
            keywords_list.append(kv)

        try:
            for options in raw['options'].split("|"):
                options_list.append(options)
        except KeyError:
            pass

        topic_object = topics.find_one({'topic_name': raw['topic']})

        question_bank.insert({'question_description': raw['question_description'],
                              'difficulty_level': raw['difficulty_level'], 'type_of_question': raw['type_of_question'],
                              'options': options_list, 'topic_id': topic_object['_id'], 'marks': raw['marks'],
                              'avg_solving_time': raw['avg_solving_time'], 'solution': raw['solution'],
                              'keywords': keywords_list})

    return {'msg': 'data uploaded successfully'}


def upload_topic(request):
    topics.insert({'topic_name': request.data['topic_name']})
    return {'msg': 'topic uploaded successfully'}




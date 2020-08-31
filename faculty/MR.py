# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 17:22:58 2020

@author: Lakshmi Subramanian
"""
from bson import ObjectId
from durable.lang import *
import numpy as np
import pandas as pd

from database_connection.helpers.collections import test_scores, topics, user_entity, question_bank

from .GA import question_set_ga


def generate_mock_test(request):
    topic_list = []
    level_list = ['Easy', 'Medium', 'Hard']
    prev_mocktests = []
    entity_object = user_entity.find_one({'login_id': request.GET.get('student_id')})
    test_score_object = test_scores.find({'student_id': entity_object['_id']}).sort([("date_of_test", -1)]).limit(1)
    all_topics_object = topics.find()
    for all_topics in all_topics_object:
        topic_list.append(all_topics['counter'])
    for test_score in test_score_object:
        for answers in test_score['question_level_marks_list']:
            topics_object = topics.find_one({'_id': answers['topic_id']})
            questions_bank_object = question_bank.find_one({'_id': ObjectId(answers['question_id'])})
            prev_mocktests.append(
                (answers['question_id'], answers['score'], answers['total'], questions_bank_object['difficulty_level'],
                 topics_object['counter']))

    question_bank_list = []
    all_questions_object = question_bank.find()
    for questions in all_questions_object:
        topic_object_id = topics.find_one({'_id': questions['topic_id']})
        question_bank_list.append([str(questions['_id']), topic_object_id['counter'], questions['difficulty_level'],
                                   questions['question_description']])

    question_bankDF = pd.DataFrame(question_bank_list,
                                   columns=['question_id', 'topic', 'difficulty_level', 'question_desc'])

    prev_mocktestsDF = pd.DataFrame(prev_mocktests,
                                    columns=['question_id', 'marks_obtained', 'total_marks', 'difficulty_level',
                                             'topic'])
    prev_mocktestsDF = prev_mocktestsDF.groupby(['topic', 'difficulty_level']).agg(
        {'marks_obtained': 'sum', 'total_marks': 'sum', 'question_id': lambda x: x.values.tolist()})
    prev_mocktestsDF['marks_percent'] = prev_mocktestsDF['marks_obtained'] / prev_mocktestsDF['total_marks']
    prev_mocktestsDF.reset_index(inplace=True)

    prev_mocktestsDF_ga = pd.DataFrame(prev_mocktests,
                                       columns=['question_id', 'marks_obtained', 'total_marks', 'difficulty_level',
                                                'topic'])
    prev_mocktestsDF_ga = prev_mocktestsDF_ga.groupby(['topic']).agg(
        {'marks_obtained': 'sum', 'total_marks': 'sum', 'question_id': lambda x: x.values.tolist()})
    prev_mocktestsDF_ga['marks_percent'] = prev_mocktestsDF_ga['marks_obtained'] / prev_mocktestsDF_ga['total_marks']

    ga_input = [1 - x for x in prev_mocktestsDF_ga['marks_percent'].to_list()]
    ga_output = question_set_ga(ga_input, 1, 20)
    ga_output = ga_output.astype(int).tolist()

    temp = prev_mocktestsDF.head(1).copy()
    temp['marks_obtained'] = 0
    temp['total_marks'] = 0
    temp['question_id'] = [[]]
    temp['marks_percent'] = 0

    for i in prev_mocktestsDF['topic'].unique():
        for j in set(level_list).difference(prev_mocktestsDF[prev_mocktestsDF['topic'] == i].difficulty_level.unique()):
            temp['topic'] = i
            temp['difficulty_level'] = j
            prev_mocktestsDF = prev_mocktestsDF.append(temp, ignore_index=True)

    with ruleset('new_mocktest_question'):
        @when_all((m.dl_score <= 10))
        def easy(c):
            easy = int(c.m.ques * 0.75) if int(c.m.ques * 0.75) != 0 else 1
            medium = c.m.ques - easy

            print("train in easy" + str(easy) + str(medium))

            prev_question_ids = prev_mocktestsDF[prev_mocktestsDF['topic'] == topic].sort_values(
                by=['difficulty_level']).question_id.to_list()
            prev_question_ids = list(set([a for b in prev_question_ids for a in b]))

            question_ids_easy = question_bankDF[(question_bankDF['topic'] == c.m.subject) & \
                                                (question_bankDF['difficulty_level'] == 'Easy') & \
                                                (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
                n=easy).question_id.tolist()

            question_set.extend(question_ids_easy)

            question_ids_medium = question_bankDF[(question_bankDF['topic'] == c.m.subject) & \
                                                  (question_bankDF['difficulty_level'] == 'Medium') & \
                                                  (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
                n=medium).question_id.tolist()

            question_set.extend(question_ids_medium)
            print(question_set)
            return question_set
            # c.assert_fact({ 'subject': c.m.subject, 'ques': 'is', 'prev_ques': 'weak' })

        @when_all((m.dl_score > 10) & (m.dl_score <= 100))
        def medium(c):
            medium = int(c.m.ques * 0.75) if int(c.m.ques * 0.75) != 0 else 1
            hard = c.m.ques - medium

            print("train in easy" + str(medium) + str(easy))

            prev_question_ids = prev_mocktestsDF[prev_mocktestsDF['topic'] == topic].sort_values(
                by=['difficulty_level']).question_id.to_list()
            prev_question_ids = list(set([a for b in prev_question_ids for a in b]))

            question_ids_medium = question_bankDF[(question_bankDF['topic'] == c.m.subject) & \
                                                  (question_bankDF['difficulty_level'] == 'Medium') & \
                                                  (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
                n=medium).question_id.tolist()

            question_set.extend(question_ids_medium)

            question_ids_hard = question_bankDF[(question_bankDF['topic'] == c.m.subject) & \
                                                (question_bankDF['difficulty_level'] == 'Hard') & \
                                                (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
                n=hard).question_id.tolist()

            question_set.extend(question_ids_hard)
            print(question_set)
            return question_set
            # c.assert_fact({ 'subject': c.m.subject, 'ques': 'is', 'prev_ques': 'weak' })

        @when_all((m.dl_score > 100))
        def hard(c):
            hard = int(c.m.ques * 0.75) if int(c.m.ques * 0.75) != 0 else 1
            medium = c.m.ques - hard

            print("train in easy" + str(hard) + str(medium))

            prev_question_ids = prev_mocktestsDF[prev_mocktestsDF['topic'] == topic].sort_values(
                by=['difficulty_level']).question_id.to_list()
            prev_question_ids = list(set([a for b in prev_question_ids for a in b]))

            question_ids_hard = question_bankDF[(question_bankDF['topic'] == c.m.subject) & \
                                                (question_bankDF['difficulty_level'] == 'Hard') & \
                                                (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
                n=hard).question_id.tolist()

            question_set.extend(question_ids_hard)

            question_ids_medium = question_bankDF[(question_bankDF['topic'] == c.m.subject) & \
                                                  (question_bankDF['difficulty_level'] == 'Medium') & \
                                                  (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
                n=medium).question_id.tolist()

            question_set.extend(question_ids_medium)
            return question_set
            # c.assert_fact({ 'subject': c.m.subject, 'ques': 'is', 'prev_ques': 'weak' })

        @when_all(+m.subject)
        def output(c):
            print('Fact: {0} {1} {2}'.format(c.m.subject, c.m.ques, c.m.dl_score))

    question_set = []
    for i in range(len(topic_list)):
        topic = topic_list[i]
        num_ques = ga_output[i]
        dl_list = prev_mocktestsDF[prev_mocktestsDF['topic'] == topic].sort_values(
            by=['difficulty_level']).marks_percent.to_list()
        dl_list01 = np.where(np.array((dl_list)) > 0.5, 1, 0).tolist()

        dl_score = dl_list01[0] + 10 * dl_list01[2] + 100 * dl_list01[1]

        assert_fact('new_mocktest_question', {'subject': topic, 'ques': num_ques, 'dl_score': dl_score})
    question_list = []
    for question_id in question_set:
        questions_object = question_bank.find_one({'_id': ObjectId(question_id)}, {'solution': 0, 'keywords': 0})
        questions_object['_id'] = str(questions_object['_id'])
        questions_object['topic_id'] = str(questions_object['topic_id'])
        question_list.append(questions_object)
    return {'msg': 'list of questions', 'question_list': question_list}

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 17:22:58 2020

@author: Lakshmi Subramanian
"""
import os
from bson import ObjectId
import numpy as np
import pandas as pd
from random import shuffle

from database_connection.helpers.collections import test_scores, topics, user_entity, question_bank

from .GA import question_set_ga
from .rulesets import *


def generate_mock_test(request):
    ruleset = {'easy': easy,
               'medium': medium,
               'hard': hard}
    try:
        topic_ids_counter = []
        level_list = ['Easy', 'Medium', 'Hard']
        prev_mocktests = []
        entity_object = user_entity.find_one({'login_id': request.GET.get('student_id')})
        test_score_object = test_scores.find({'student_id': entity_object['_id']}).sort([("date_of_test", -1)]).limit(1)
        for test_score in test_score_object:
            for answers in test_score['question_level_marks_list']:
                topics_object = topics.find_one({'_id': answers['topic_id']})
                questions_bank_object = question_bank.find_one({'_id': ObjectId(answers['question_id'])})
                prev_mocktests.append(
                    (answers['question_id'], answers['score'], answers['total'], questions_bank_object['difficulty_level'],
                     topics_object['counter']))
                topic_ids_counter.append(topics_object['counter'])

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

        question_set = []
        for i in range(len(prev_mocktestsDF_ga.index)):
            dl = pd.read_csv(os.getcwd()+r'/difficulty_level.csv')
            topic = prev_mocktestsDF_ga.index[i]
            num_ques = ga_output[i]
            dl_list = prev_mocktestsDF[prev_mocktestsDF['topic'] == topic].sort_values(
                by=['difficulty_level']).marks_percent.to_list()
            dl_list01 = np.where(np.array((dl_list)) > 0.5, 1, 0).tolist()
            topic_difficulty_level = dl[
                (dl['hard'] == np.int64(dl_list01[1])) & (dl['medium'] == np.int64(dl_list01[2])) & (
                            dl['easy'] == np.int64(dl_list01[0]))]['difficulty_level'].item()
            questions_topic = ruleset[topic_difficulty_level](topic, num_ques, prev_mocktestsDF, question_bankDF)
            question_set.extend(questions_topic)

        question_bankDF[question_bankDF['question_id'].isin(question_set)].groupby(['topic']).agg({'question_id': 'count'})
        print(question_set)
        question_list = []
        for question_id in question_set:
            questions_object = question_bank.find_one({'_id': ObjectId(question_id)}, {'solution': 0, 'keywords': 0})
            questions_object['_id'] = str(questions_object['_id'])
            topic_object = topics.find_one({'_id': questions_object['topic_id']})
            questions_object['topic_name'] = topic_object['topic_name']
            questions_object['topic_id'] = str(questions_object['topic_id'])
            question_list.append(questions_object)
        shuffle(question_list)
        return {'msg': 'list of questions', 'question_list': question_list, 'status': True}
    except :
        return {'msg': 'unable to generate mock test', 'status': False}


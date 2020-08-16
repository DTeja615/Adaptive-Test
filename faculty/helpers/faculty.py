import pandas as pd
import numpy as np
from django.contrib.auth.hashers import make_password, check_password

from faculty.GA import question_set_ga
from database_connection.helpers.collections import user_entity, question_bank, test_scores, topics


def upload_faculty_details(request):
    try:
        request.data['password'] = create_sha256_password(request.data['password'])
        user_entity.insert(request.data)
        return {'msg': 'entity data uploaded', 'status': True}
    except:
        return {'msg': 'unable to upload details, please try again', 'status': False}


def faculty_login(request):
    entity_object = user_entity.find_one({'login_id': request.GET.get('login_id')})
    if entity_object:
        bool_value = check_password(request.GET.get('password'), entity_object['password'])
        if bool_value is True:
            return {'msg': 'login successful', 'status': True}
        else:
            return {'msg': 'login id or password is wrong', 'status': False}
    else:
        return {'msg': 'entity does not exist', 'status': False}


def faculty_upload_question(request):
    try:
        question_bank.insert(request.data)
        return {'msg': 'question uploaded successfully', 'status': True}
    except:
        return {'msg': 'could not upload question', 'status': False}


def update_student_scores(request):
    try:
        entity_object = user_entity.find_one({'login_id': request.data['student_id']})
        test_score_object = test_scores.find_one({'student_id': entity_object['_id']})
        for questions in test_score_object['question_level_marks_list']:
            for scores in request.data['question_level_marks_list']:
                if questions['question_id'] == scores['question_id']:
                    questions['score'] = scores['score']

        test_scores.update_one({'student_id': entity_object['_id']}, {'$set':
                                                                          {'total_marks_obtained.marks_obtained':
                                                                               request.data['total_marks_obtained'][
                                                                                   'marks_obtained'],
                                                                           'question_level_marks_list':
                                                                               test_score_object[
                                                                                   'question_level_marks_list']}})
        return {'msg': 'test scores updated successfully', 'status': True}
    except:
        return {'msg': 'could not update test scores', 'status': False}


def generate_mock_test(request):
    dataframe = {}
    try:
        entity_object = user_entity.find_one({'login_id': request.GET.get('student_id')})
        test_score_object = test_scores.find({'student_id': entity_object['_id']}).sort([("date_of_test", -1)]).limit(1)
        test_object_list = [doc for doc in test_score_object]
        for test_object in test_object_list:
            for scores in test_object['question_level_marks_list']:
                del scores['question_id']
                del scores['student_answer']
                topic_object = topics.find_one({'_id': scores['topic_id']})
                scores['topic_id'] = topic_object['counter']
            dataframe = pd.DataFrame.from_records(test_object['question_level_marks_list']).astype(int).groupby(
                'topic_id').sum().T.to_dict()
        score_list = []
        for i in range(1, len(dataframe)+1):
            try:
                score_list.append(dataframe[i]['score'] / dataframe[i]['total'])
            except:
                pass
        questions_list = []
        model_output = question_set_ga([1-x for x in np.array(score_list)])
        for i in range(1, len(dataframe)+1):
            try:
                test_score_object = topics.find_one({'counter': i})
                if test_score_object:
                    number_of_questions = int(model_output[0])
                    model_output = np.delete(model_output, 0)
                    questions_cursor = question_bank.find({'topic_id': test_score_object['_id']}, {'solution': 0, 'keywords': 0}).limit(number_of_questions)
                    for questions in questions_cursor:
                        questions['_id'] = str(questions['_id'])
                        questions['topic_id'] = str(questions['topic_id'])
                        questions_list.append(questions)
                else:
                    continue
            except:
                pass
        return {'msg': 'list of questions', 'questions_list': questions_list, 'status': True}
    except:
        return {'msg': 'unable to generate mock test', 'status': False}


def create_sha256_password(password):
    password = make_password(password)
    return password

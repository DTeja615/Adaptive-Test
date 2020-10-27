import datetime
import pymongo
from bson import ObjectId
from django.contrib.auth.hashers import make_password, check_password

from .link_scaper import link_scraping
from database_connection.helpers.collections import user_entity, test_scores, question_bank


def upload_student_details(request):
    try:
        request.data['password'] = create_sha256_password(request.data['password'])
        user_entity.insert(request.data)
        return {'msg': 'entity data uploaded', 'status': True}
    except:
        return {'msg': 'unable to upload details, please try again', 'status': False}


def student_login(request):
    entity_object = user_entity.find_one({'login_id': request.GET.get('login_id')})
    if entity_object:
        bool_value = check_password(request.GET.get('password'), entity_object['password'])
        if bool_value is True:
            return {'msg': 'login successful', 'status': True}
        else:
            return {'msg': 'login id or password is wrong', 'status': False}
    else:
        return {'msg': 'entity does not exist', 'status': False}


def upload_student_answers(request):
    try:
        entity_object = user_entity.find_one({'login_id': request.data['student_id']})
        for question_object in request.data['question_level_marks_list']:
            question_bank_object = question_bank.find_one({'_id': ObjectId(question_object['question_id'])})
            question_object['total'] = int(question_bank_object['marks'])
            question_object['topic_id'] = question_bank_object['topic_id']
        test_scores.insert({'student_id': entity_object['_id'],
                            'total_marks_obtained': request.data['total_marks_obtained'],
                            'question_level_marks_list': request.data['question_level_marks_list'],
                            'date_of_test': datetime.datetime.now()})
        return {'msg': 'test details uploaded successfully', 'status': True}
    except:
        return {'msg': 'could not upload test details', 'status': False}


def previous_scores(request):
    previous_test_scores_list = []
    try:
        user_entity_object = user_entity.find_one({'login_id': request.GET.get('student_id')})
        previous_scores_object = test_scores.find({'student_id': user_entity_object['_id']},
                                                  {'question_level_marks_list.topic_id': 0}).sort([
            ('date_of_test', pymongo.DESCENDING)])
        for previous_test_scores in previous_scores_object:
            previous_test_scores['student_id'] = str(previous_test_scores['student_id'])
            previous_test_scores['_id'] = str(previous_test_scores['_id'])
            previous_test_scores['date_of_test'] = str(previous_test_scores['date_of_test'].day) + '/' + \
                                                   str(previous_test_scores['date_of_test'].month) + '/' + \
                                                   str(previous_test_scores['date_of_test'].year)
            for answers in previous_test_scores['question_level_marks_list']:
                question_bank_object = question_bank.find_one({'_id': ObjectId(answers['question_id'])})
                answers['solution'] = question_bank_object['solution']
                answers['keywords'] = "Keywords to include "+str(question_bank_object['keywords'])
                answers['question'] = question_bank_object['question_description']
                link_list = link_scraping(answers['question'])
                answers['list_of_links'] = link_list
            previous_test_scores_list.append(previous_test_scores)

        return {'msg': 'previous test scores', 'status': True, 'list': previous_test_scores_list}
    except:
        return {'msg': 'unable to get test scores', 'status': False}


def create_sha256_password(password):
    password = make_password(password)
    return password

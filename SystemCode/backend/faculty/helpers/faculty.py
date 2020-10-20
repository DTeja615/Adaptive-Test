from bson import ObjectId
from django.contrib.auth.hashers import make_password, check_password

from database_connection.helpers.collections import user_entity, question_bank, test_scores


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
        test_score_object = test_scores.find({'student_id': entity_object['_id']}).sort([('date_of_test', -1)]).limit(1)
        test_data_dict = dict()
        for test_object in test_score_object:
            test_data_dict = test_object
        for questions in test_data_dict['question_level_marks_list']:
            for scores in request.data['question_level_marks_list']:
                if questions['question_id'] == scores['question_id']:
                    questions['score'] = scores['score']

        test_scores.update_one({'student_id': entity_object['_id'], 'date_of_test': test_data_dict['date_of_test']},
                                                                          {'$set':
                                                                          {'total_marks_obtained.marks_obtained':
                                                                               request.data['total_marks_obtained'][
                                                                                   'marks_obtained'],
                                                                           'question_level_marks_list':
                                                                               test_data_dict[
                                                                                   'question_level_marks_list']}})
        return {'msg': 'test scores updated successfully', 'status': True}
    except:
        return {'msg': 'could not update test scores', 'status': False}


def fetch_mock_test(request):
    previous_answers_list = []
    try:
        user_entity_object = user_entity.find_one({'login_id': request.GET.get('student_id')})
        previous_answers_object = test_scores.find({'student_id': user_entity_object['_id']},
                                                  {'question_level_marks_list.topic_id': 0,
                                                   'date_of_test': 0}).sort([
            ('date_of_test', -1)]).limit(1)
        for previous_answers in previous_answers_object:
            previous_answers['student_id'] = str(previous_answers['student_id'])
            previous_answers['_id'] = str(previous_answers['_id'])
            for questions in previous_answers['question_level_marks_list']:
                question_object = question_bank.find_one({'_id': ObjectId(questions['question_id'])})
                questions['question'] = question_object['question_description']
            previous_answers_list.append(previous_answers)

        return {'msg': 'previous test answers', 'status': True, 'list': previous_answers_list}
    except:
        return {'msg': 'unable to get test answers', 'status': False}


def create_sha256_password(password):
    password = make_password(password)
    return password

import datetime
from django.contrib.auth.hashers import make_password, check_password

from database_connection.helpers.collections import user_entity, test_scores


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
        test_scores.insert({'student_id': entity_object['_id'],
                            'total_marks_obtained': request.data['total_marks_obtained'],
                            'question_level_marks_list': request.data['question_level_marks_list'],
                            'date_of_test': datetime.datetime.now()})
        return {'msg': 'test details uploaded successfully', 'status': True}
    except :
        return {'msg': 'could not upload test details', 'status': False}


def create_sha256_password(password):
    password = make_password(password)
    return password
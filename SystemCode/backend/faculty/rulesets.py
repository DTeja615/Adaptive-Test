def easy(topic, ques, prev_mocktestsDF, question_bankDF):
    question_set = []
    easy = int(ques * 0.75) if int(ques * 0.75) != 0 else 1
    medium = ques - easy

    print("train in easy" + str(easy) + str(medium))

    prev_question_ids = prev_mocktestsDF[prev_mocktestsDF['topic'] == topic].sort_values(
        by=['difficulty_level']).question_id.to_list()
    prev_question_ids = list(set([a for b in prev_question_ids for a in b]))

    question_ids_easy = question_bankDF[(question_bankDF['topic'] == topic) & \
                                        (question_bankDF['difficulty_level'] == 'Easy') & \
                                        (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
        n=easy).question_id.tolist()

    question_set.extend(question_ids_easy)

    question_ids_medium = question_bankDF[(question_bankDF['topic'] == topic) & \
                                          (question_bankDF['difficulty_level'] == 'Medium') & \
                                          (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
        n=medium).question_id.tolist()

    question_set.extend(question_ids_medium)
    print(question_set)
    return question_set


def medium(topic, ques, prev_mocktestsDF, question_bankDF):
    question_set = []
    medium = int(ques * 0.75) if int(ques * 0.75) != 0 else 1
    hard = ques - medium

    print("train in easy" + str(medium) + str(easy))

    prev_question_ids = prev_mocktestsDF[prev_mocktestsDF['topic'] == topic].sort_values(
        by=['difficulty_level']).question_id.to_list()
    prev_question_ids = list(set([a for b in prev_question_ids for a in b]))

    question_ids_medium = question_bankDF[(question_bankDF['topic'] == topic) & \
                                          (question_bankDF['difficulty_level'] == 'Medium') & \
                                          (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
        n=medium).question_id.tolist()

    question_set.extend(question_ids_medium)

    question_ids_hard = question_bankDF[(question_bankDF['topic'] == topic) & \
                                        (question_bankDF['difficulty_level'] == 'Hard') & \
                                        (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
        n=hard).question_id.tolist()

    question_set.extend(question_ids_hard)
    print(question_set)
    return question_set


def hard(topic, ques, prev_mocktestsDF, question_bankDF):
    question_set = []
    hard = int(ques * 0.75) if int(ques * 0.75) != 0 else 1
    medium = ques - hard

    print("train in easy" + str(hard) + str(medium))

    prev_question_ids = prev_mocktestsDF[prev_mocktestsDF['topic'] == topic].sort_values(
        by=['difficulty_level']).question_id.to_list()
    prev_question_ids = list(set([a for b in prev_question_ids for a in b]))

    question_ids_hard = question_bankDF[(question_bankDF['topic'] == topic) & \
                                        (question_bankDF['difficulty_level'] == 'Hard') & \
                                        (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
        n=hard).question_id.tolist()

    question_set.extend(question_ids_hard)

    question_ids_medium = question_bankDF[(question_bankDF['topic'] == topic) & \
                                          (question_bankDF['difficulty_level'] == 'Medium') & \
                                          (~question_bankDF['question_id'].isin(prev_question_ids))].sample(
        n=medium).question_id.tolist()

    question_set.extend(question_ids_medium)
    print(question_set)
    return question_set

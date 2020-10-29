import numpy as np
from geneticalgorithm import geneticalgorithm


# past scores
# assumption her is variables i.e topics are in a particular fashion
# P - is the array of (sum of all scores obtained in a topic)/(sum of total marks of the questions in the topic)
#    for every topic in topic list, if a particular topic has not been tested before the value to be filled is 0
# min_question_topic - the minimum number of questions per topic for mock test
# total_questions - total number of question for the mock test

def question_set_ga(P, min_question_topic=1, total_questions=20):
    total_topics = len(P)

    def f(X):
        pen = 0
        p_ratio = np.array([i / sum(P) for i in P])
        x_ratio = np.array([i / sum(X) for i in X])
        pen = pen + 5 * abs(sum(X) - total_questions)

        if np.sum(X) > total_questions:
            pen = pen + 500 + 1000 * (sum(X) - total_questions)

        return np.sum(abs(p_ratio - x_ratio)) + pen

    varbound = np.array([[min_question_topic, 20]] * total_topics)

    algorithm_param = {'max_num_iteration': 250,
                       'population_size': 200,
                       'mutation_probability': 0.1,
                       'elit_ratio': 0.01,
                       'crossover_probability': 0.5,
                       'parents_portion': 0.3,
                       'crossover_type': 'uniform',
                       'max_iteration_without_improv': None}

    model = geneticalgorithm(function=f, dimension=total_topics, variable_type='int',
                             variable_boundaries=varbound, algorithm_parameters=algorithm_param)
    model.run()
    return model.output_dict['variable']


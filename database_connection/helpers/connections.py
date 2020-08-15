import pymongo

from django.conf import settings

mongo_connection = None


def mongodb_connection():

    global mongo_connection
    if mongo_connection:
        return mongo_connection
    else:
        client = pymongo.MongoClient(settings.MONGO_DB)
        mongo_connection = client[settings.MONGO_DB_NAME]
        return mongo_connection


db = mongodb_connection()

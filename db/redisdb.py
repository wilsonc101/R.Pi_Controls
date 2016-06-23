#!/usr/bin/python -B

import redis

REDIS_SERVER = "localhost"
REDIS_SERVER_PORT = 6379
REDIS_DB = 0

REDIS_CONNECTION = redis.StrictRedis(host=REDIS_SERVER,
                                     port=REDIS_SERVER_PORT,
                                     db=REDIS_DB)


def deleteObject(id):
    REDIS_CONNECTION.delete(id)

    return True


def getObject(id):
    redis_object = REDIS_CONNECTION.get(id)

    if redis_object:
        redis_object = redis_object.decode('utf-8')

    return redis_object


def getObjects(key="relay*"):
    objects = {}
    object_ids = REDIS_CONNECTION.keys(key)

    for id in object_ids:
        id = id.decode('utf-8')
        object = getObject(id)
        if object:
            objects[id] = object

    return objects

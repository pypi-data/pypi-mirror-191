import redis


def get_redis_config(db=0):
    return {'db': 0}


class RedisConfig:
    def __init__(self, db=0):
        self.db = db


def get_redis_instance(redis_config: RedisConfig = RedisConfig()):
    return redis.StrictRedis(decode_responses=True, db=redis_config.db)

# import redis
# import sys
# from datetime import timedelta


# def redis_connect() -> redis.client.Redis:
#     try:
#         client = redis.Redis(
#             host="localhost",
#             port=6379,
#             password="ubuntu",
#             db=0,
#             socket_timeout=5,
#         )
#         ping = client.ping()
#         if ping is True:
#             return client
#     except redis.AuthenticationError:
#         print("AuthenticationError")
#         sys.exit(1)



# client = redis_connect()


# def get_routes_from_cache(key: str) -> str:
#     """Get data from redis."""

#     val = client.get(key)
#     return val


# def set_routes_to_cache(key: str, value: str) -> bool:
#     """Set data to redis."""

#     state = client.setex(key, timedelta(seconds=3600), value=value, )
#     return state
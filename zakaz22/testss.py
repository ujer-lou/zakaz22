import redis

try:
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    r.ping()
    print("Connected to Redis!")
except redis.ConnectionError as e:
    print("Redis connection failed:", e)

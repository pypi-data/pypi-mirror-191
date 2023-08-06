from functools import wraps

def future_tense(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"future_tense：{func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper

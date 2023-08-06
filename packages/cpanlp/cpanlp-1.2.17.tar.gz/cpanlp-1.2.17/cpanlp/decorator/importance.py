from functools import wraps
def importance(importance):
    def important_annotatio(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Importance_Level {importance}")
            return func(*args, **kwargs)
        return wrapper
    return important_annotatio

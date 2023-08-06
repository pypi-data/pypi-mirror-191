from functools import wraps
def prob(probability):
    def estimated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            func.probability =probability
            print(f"Estimate probability of {probability}: {result}")
            return result
        return wrapper
    return estimated

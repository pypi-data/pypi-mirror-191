from functools import wraps
def with_side_effects(side_effects):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            fn.side_effects = side_effects
            print("Possible Side Effects:")
            if hasattr(fn, 'side_effects'):
                for effect in fn.side_effects:
                    print(f"- {effect}")
            return result
        return wrapper
    return decorator
side_effects=["financial instability","loss of reputation","decreased employee morale","Increased risk of default.","Amplified losses","Increased volatility","Difficulty in repaying debt","Reduced flexibility","loss of relationships with investors"]
def with_positive_effects(positive_effects):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            fn.positive_effects = positive_effects
            print("Possible Positive Effects:")
            if hasattr(fn, 'positive_effects'):
                for effect in fn.positive_effects:
                    print(f"- {effect}")
            return result
        return wrapper
    return decorator

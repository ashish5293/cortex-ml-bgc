from functools import wraps

from app.config import Config



def exception_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except BaseException as e:
            print(f'{func.__name__} failed: {e.__str__()}')
    return wrapper

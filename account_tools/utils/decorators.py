# utils/decorators.py
import logging
from functools import wraps

def log_de_erro(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Erro em {func.__name__}: {e}")
            return None
    return wrapper
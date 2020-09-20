# from https://stackoverflow.com/questions/17237857/python3-singleton-metaclass-method-not-working/17237903
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

import functools


class InstanceCreationError(Exception):
    pass


class Constant(type):
    def __new__(cls, name, bases, arg):
        def _raise_error(x):
            raise InstanceCreationError(
                f"Cannot create an instance of {x.__class__.__name__}"
            )

        inst = super().__new__(cls, name, bases, {"_Constant__frozen": False, **arg})
        inst.__init__ = _raise_error
        inst.__frozen = True
        return inst

    def __setattr__(self, key, value):
        if self.__frozen:
            raise AttributeError("Cannot set or change the class attributes")
        super().__setattr__(key, value)

    def __str__(cls):
        return cls.__name__

    def __repr__(cls):
        return cls.__name__


def constant(cls):
    __name = str(cls.__name__)
    __bases = tuple(cls.__bases__)
    __dict = dict(cls.__dict__)

    for each_slot in __dict.get("__slots__", tuple()):
        __dict.pop(each_slot, None)

    __dict["__metaclass__"] = Constant
    __dict["__wrapped__"] = cls
    return Constant(__name, __bases, __dict)


def dispatch(func):
    dispatch_map = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = args[0]
        if key in dispatch_map:
            return dispatch_map[key](*args[1:], **kwargs)
        return func(*args, **kwargs)

    def register(key):
        def decorator(func_):
            dispatch_map[key] = func_
            return func_

        return decorator

    wrapper.register = register
    return wrapper

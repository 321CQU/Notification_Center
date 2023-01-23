__all__ = ['SingletonType']


class SingletonType(type):
    instance = {}

    def __call__(cls, *args, **kwargs):
        if cls.__name__ not in SingletonType.instance.keys():
            SingletonType.instance[cls.__name__] = super(SingletonType, cls).__call__(*args, **kwargs)
        return SingletonType.instance[cls.__name__]

def sorted_class_attribute(vars_names):
    def decorator(class_to_dec):
        class NewCls(object):
            def __init__(self, *args, **kwargs):
                self.inst = class_to_dec(*args, **kwargs)

            def __getattribute__(self, item):
                try:
                    x = super(NewCls, self).__getattribute__(item)
                except AttributeError:
                    pass
                else:
                    return x

                x = self.inst.__getattribute__(item)
                # if the item isn't method
                if type(x) != type(self.__init__):
                    if item in vars_names:
                        return sorted(x)
                return x
    return decorator

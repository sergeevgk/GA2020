_CATEGORIES = dict()


def get_all_classes_for_category(category_name):
    return _CATEGORIES[category_name]


def category_class_attribute(name):
    def decorator(class_to_dec):
        if name in _CATEGORIES.keys():
            _CATEGORIES[name].append(class_to_dec)
        else:
            _CATEGORIES[name] = [class_to_dec]

        def category_getter(self):
            return name

        setattr(class_to_dec, 'get_category', category_getter)
    return decorator

from django.template.defaultfilters import register


@register.filter(name='get_first_item')
def get_first_item(dictionary, key):
    try:
        x = dictionary.get(key, '#ffffff')[0]
    except IndexError:
        x = dictionary.get(key, '#ffffff')
    return x


@register.filter(name='get_second_item')
def get_second_item(dictionary, key):
    try:
        x = dictionary.get(key, '')[1]
    except IndexError:
        x = dictionary.get(key, '')
    return x

#we will create one Custom filter in myfilters.py

from django import template
register=template.Library()

@register.filter
def get(mapping,key): # mapping is the dictonary,we want to pass the value from the key
    return mapping.get(key, '')
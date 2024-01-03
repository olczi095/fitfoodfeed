from django import template
import os

register = template.Library()

@register.filter(name='file_exists')
def file_exists(value):
    return os.path.isfile(value)

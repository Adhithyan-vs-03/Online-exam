from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None

# Online_App/custom_filters.py
from django import template
import re

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split a string by the given delimiter"""
    if value and delimiter:
        return value.split(delimiter)
    return []

@register.filter
def split_string(value, delimiter):
    """Split a string by the given delimiter for fill-in-the-blanks"""
    if value and delimiter:
        # Split and include empty strings for consecutive delimiters
        parts = re.split(f'({re.escape(delimiter)})', value)
        # Filter out empty delimiter markers
        return [part for part in parts if part != delimiter]
    return [value]
from django import template

register = template.Library()

@register.filter
def filter_notification_type(notifications, notification_type):
    """Filter notifications by type"""
    return [n for n in notifications if n.notification_type == notification_type]

@register.filter
def pluralize(value):
    """Add 's' if value is not 1"""
    return 's' if value != 1 else ''
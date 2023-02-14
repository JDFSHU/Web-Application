from django import template


register = template.Library()

@register.filter
def stars(value):
    full_stars = int(value)
    empty_stars = 5 - full_stars
    return '⭐' * full_stars + '☆' * empty_stars
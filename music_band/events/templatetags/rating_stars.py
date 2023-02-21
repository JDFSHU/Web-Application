from django import template

# This is a custom template filter that will be used to display the rating stars instead of int values
register = template.Library()
@register.filter
def stars(value):
    full_stars = int(value)
    empty_stars = 5 - full_stars
    return '⭐' * full_stars + '☆' * empty_stars
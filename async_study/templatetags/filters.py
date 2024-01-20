from django import template

register = template.Library()


@register.filter
def return_flashcard_object(value):
    return {"flashcard": value}

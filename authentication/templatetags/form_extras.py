from django import template

register = template.Library()


@register.filter
def first_error_message(value):
    """ Retourner le premier message d'erreur du formulaire """
    for field in value:
        return value[field][0]
    return None

from django import template

register = template.Library()

@register.filter
def has_tag(user, tag_code):
    if not user.is_authenticated:
        return False

    return user.tags.filter(tag__code=tag_code).exists()

""""

Example usage

{% load user_tags %}

{% if request.user|has_tag:"gallery_manager" %}
    <a href="/gallery/upload/">Upload Image</a>
{% endif %}

"""
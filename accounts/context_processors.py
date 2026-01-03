def user_tags(request):
    if not request.user.is_authenticated:
        return {}

    tags = set(
        request.user.tags.values_list("tag__code", flat=True)
    )

    return {
        "USER_TAGS": tags
    }

"""

Use it anywhere

{% if "attendance_manager" in USER_TAGS %}
    <li>Attendance</li>
{% endif %}

"""

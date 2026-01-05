def user_tags(request):
    if request.user.is_authenticated:
        tags = set(
            request.user.tags.values_list("tag__code", flat=True)
        )
    else:
        tags = set()

    return {
        "USER_TAGS": tags
    }
"""

Use it anywhere

{% if "attendance_manager" in USER_TAGS %}
    <li>Attendance</li>
{% endif %}

"""

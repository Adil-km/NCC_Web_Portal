def user_has_tag(user, tag_code):
    if not user.is_authenticated:
        return False

    return user.tags.filter(tag__code=tag_code).exists()


"""
###Example use case

from django.http import HttpResponseForbidden
from accounts.utils import user_has_tag

def attendance_dashboard(request):
    if not user_has_tag(request.user, "attendance_manager"):
        return HttpResponseForbidden("You are not allowed")

    return render(request, "attendance/dashboard.html")

    
"""
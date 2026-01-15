import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Activity, Attendance

User = get_user_model()

@ensure_csrf_cookie
def mark_attendance(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_list = data.get('attendance_data', [])
            
            # Efficiently update or create records
            for entry in attendance_list:
                user_id = entry.get('user_id')
                status = entry.get('status')
                
                if user_id and status:
                    Attendance.objects.update_or_create(
                        user_id=user_id,
                        activity=activity,
                        defaults={'status': status}
                    )
            
            return JsonResponse({'status': 'success', 'message': 'Attendance marked successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # --- GET Request Logic ---
    
    # Get all users (You might want to filter this, e.g., User.objects.filter(is_cadet=True))
    users = User.objects.all().order_by('username')
    
    # Get existing attendance for this activity to pre-fill the form
    existing_attendance = Attendance.objects.filter(activity=activity)
    # Create a dictionary for O(1) lookup: {user_id: 'PRESENT'}
    attendance_map = {att.user_id: att.status for att in existing_attendance}

    # Prepare list for template
    cadet_list = []
    for user in users:
        cadet_list.append({
            'user': user,
            'current_status': attendance_map.get(user.id) # Will be None, 'PRESENT', or 'ABSENT'
        })

    context = {
        'activity': activity,
        'cadet_list': cadet_list,
    }
    return render(request, 'dashboard/mark_attendance.html', context)
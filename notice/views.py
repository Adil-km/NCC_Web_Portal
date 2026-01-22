from django.shortcuts import redirect, render

from notice.forms import NoticeForm
from notice.models import Notice

# Create your views here.


def notice(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'dashboard/notice.html', {
        'notices': notices
    })

def upload_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_notice')
    else:
        form = NoticeForm()

    return render(request, 'dashboard/upload_notice.html', {'form': form})

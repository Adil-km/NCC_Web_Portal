```
python manage.py shell
```

```python
from your_app_name.models import UserTag

tags = [
    {
        "name": "Website Manager",
        "code": "website_manager",
        "description": "Can add and update images displayed on the public website (eg. slider images, about section image, etc.)."
    },
    {
        "name": "Attendance Marker",
        "code": "attendance_marker",
        "description": "Can mark attendance for assigned cadets during NCC events."
    },
    {
        "name": "Downloads Manager",
        "code": "downloads_manager",
        "description": "Can upload and manage files in the cadet downloads section."
    },
    {
        "name": "Gallery Manager",
        "code": "gallery_manager",
        "description": "Can upload, edit, and manage images in the public NCC photo gallery."
    },
    {
        "name": "News Editor",
        "code": "news_editor",
        "description": "Can create, edit, and publish internal and public news and events."
    },
]

for tag in tags:
    obj, created = UserTag.objects.get_or_create(
        code=tag["code"],
        defaults={
            "name": tag["name"],
            "description": tag["description"]
        }
    )
    if created:
        print(f"Created: {obj.name}")
    else:
        print(f"Already exists: {obj.name}")

```

## User Tags
Achievements Manager
achievements_manager
Can add and update NCC achievements displayed on the public website.

Attendance Marker
attendance_marker
Can mark attendance for assigned cadets during NCC events.

Attendance Viewer
attendance_viewer
Can view and download attendance reports beyond assigned cadets.

Downloads Manager
downloads_manager
Can upload and manage files in the cadet downloads section.

Gallery Manager
gallery_manager
Can upload, edit, and manage images in the public NCC photo gallery.

News Editor
news_editor
Can create, edit, and publish internal and public news and events.


# Env

DEV=True

# postgres Database 
NAME=postgres
USER=postgres
PASSWORD=
HOST=localhost

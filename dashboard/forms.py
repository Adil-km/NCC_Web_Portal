from django import forms
from django.contrib.auth.models import Group, Permission
from accounts.models import User, UserTag, UserTagAssignment

class AssignTagsForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select User"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=UserTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Tags"
    )

    def __init__(self, *args, **kwargs):
        selected_user = kwargs.pop('selected_user', None)
        super().__init__(*args, **kwargs)

        # Pre-select currently assigned tags
        if selected_user:
            self.fields['tags'].initial = selected_user.tags.values_list('tag_id', flat=True)

    def save(self):
        user = self.cleaned_data['user']
        selected_tags = self.cleaned_data['tags']

        print("USER:", user.username)
        print("SELECTED TAGS:", [t.code for t in selected_tags])
        
        # Safely assign tags (avoid duplicates)
        existing_tag_ids = set(user.tags.values_list('tag_id', flat=True))
        new_tag_ids = set(tag.id for tag in selected_tags)

        # Add new tags
        for tag_id in new_tag_ids - existing_tag_ids:
            UserTagAssignment.objects.create(user=user, tag_id=tag_id)

        # Remove unchecked tags
        for tag_id in existing_tag_ids - new_tag_ids:
            UserTagAssignment.objects.filter(user=user, tag_id=tag_id).delete()

class AssignUserRoleForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select User"
    )
    role = forms.ChoiceField(
        choices=User.Role.choices,
        label="Select Role"
    )

class AssignGroupForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())

class CreateGroupWithPermissionsForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label="Group Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter new role name"})
    )

    permissions = forms.ModelMultipleChoiceField(
        # queryset=Permission.objects.filter(content_type__app_label="accounts"),
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Permissions"
    )


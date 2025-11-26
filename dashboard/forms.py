from django import forms
from django.contrib.auth.models import Group, Permission
from accounts.models import User  

class AssignRoleForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select User"
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Select Role / Group"
    )

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
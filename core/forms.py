from django import forms
from .models import Room


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'host_name', 'description', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Morning Standup', 'class': 'form-input', 'data-i18n-placeholder': 'create.name_ph'}),
            'host_name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'form-input', 'data-i18n-placeholder': 'create.host_ph'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional description...', 'class': 'form-input', 'rows': 3, 'data-i18n-placeholder': 'create.desc_ph'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Leave blank for open room', 'class': 'form-input', 'data-i18n-placeholder': 'create.pw_ph'}, render_value=True),
        }
        labels = {
            'name': 'Room Name',
            'host_name': 'Your Name (Host)',
            'description': 'Description (optional)',
            'password': 'Room Password (optional)',
        }


class JoinRoomForm(forms.Form):
    code = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'placeholder': 'Enter room code (e.g. ABC123XYZ)', 'class': 'form-input code-input', 'data-i18n-placeholder': 'join.code_ph'})
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your display name', 'class': 'form-input', 'data-i18n-placeholder': 'join.name_ph'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Room password (if required)', 'class': 'form-input', 'data-i18n-placeholder': 'join.pw_ph'})
    )

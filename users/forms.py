from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminUserCreationForm
from .models import CustomUser


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = CustomUser
        fields = "__all__"
    
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = "__all__"

from django.contrib import admin
from users.models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import  Profile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ("username","email", "is_active", "is_staff")
    # # list_display_links = ("username","school_id")
    
    # fieldsets = UserAdmin.fieldsets + (
    #     ("Extra Info", {"fields": ("role","school_id","department")}),
    # )
    
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email','password1', 'password2')}
    #     ),
    # )

admin.site.register(CustomUser, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")
    
    
    
admin.site.register(Profile, ProfileAdmin)
from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("sign-in/",views.sign_in, name="sign-in"),
    path("sign-up/",views.sign_up, name="sign-up"),
    path("profile/",views.profile, name="profile"),
    path("password-reset/",views.password_reset, name="password-reset"),
    path("password-update/",views.password_update, name="password-update"),
]


htmx_patterns = [
    path("check-email/", views.check_email, name="check-email")
]

urlpatterns += htmx_patterns
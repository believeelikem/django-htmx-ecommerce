import re
from django.contrib.auth import get_user_model

User = get_user_model()

def validate_user_input(view_func):
    def view_func_wrapper(request):
        message = ""
        color = "red"
        if request.method == "GET": 
            if request.GET.get("email-for-sign-in",""):
                email_entered = request.GET["email-for-sign-in"]
                print("email entered is = ",email_entered)
                print()
                if User.objects.filter(
                    email = email_entered).exists():
                    message = "✅"
                    color = "green"
                else:
                    message = "no user with email '%s' exists" % email_entered
                    
        
        context  = {
            "color":color,
            "message":message
        } 
        return view_func(request, context)     
    
    return view_func_wrapper
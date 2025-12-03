from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from .models import *

admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

class ProductAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

admin.site.register(Product, ProductAdmin)

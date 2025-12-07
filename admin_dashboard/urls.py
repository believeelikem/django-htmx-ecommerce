from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),
    path("orders/", views.admin_orders, name="admin-orders"),
    path("orders/detail/", views.admin_order_detail, name="admin-order-detail"),
    path("products/", views.admin_products, name="admin-products"),
    path("products/add/", views.admin_product_edit, name="admin-product-edit"),
    path("customers/", views.admin_customers, name="admin-customers"),
    path("settings/", views.admin_settings, name="admin-settings"),
    path("sign-in/", views.admin_sign_in, name="admin-sign-in"),
    path("forgot-password/", views.admin_forgot_password, name="admin-forgot-password"),
]


htmx_patterns = [
    path("validate/", views.validate_product_error, name="validate-product-error")
]

urlpatterns += htmx_patterns
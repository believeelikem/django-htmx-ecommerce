from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin-dashboard"),
    path("orders/", views.admin_orders, name="admin-orders"),
    path("orders/detail/", views.admin_order_detail, name="admin-order-detail"),
    path("products/", views.admin_products, name="admin-products"),
    path("products/add/", views.admin_product_add, name="admin-product-add"),
    path("customers/", views.admin_customers, name="admin-customers"),
    path("settings/", views.admin_settings, name="admin-settings"),
    path("sign-in/", views.admin_sign_in, name="admin-sign-in"),
    path("forgot-password/", views.admin_forgot_password, name="admin-forgot-password"),
]


htmx_patterns = [
    path("validate/", views.validate_product_add_error, name="validate-product-error"),
    path("add-product-to-list/", views.add_product_to_list, name = "add-product-to-list"),
    path("create-product/", views.create_product, name = "create-product"),
    path("delete-product/<int:id>", views.delete_product_from_list, name = "delete-post-single")
]

urlpatterns += htmx_patterns
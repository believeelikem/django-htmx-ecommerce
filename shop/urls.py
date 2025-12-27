from django.urls import path
from shop import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.cart, name="cart"),
    path("products/", views.products, name="products"),
    # path("products/detail/", views.product_detail, name="product-detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("user-dashboard/", views.user_dashboard, name="dashboard"),
]


htmx_patterns = [
    path("products/<slug:slug>/detail/", views.product_detail, name="product-detail"),
    path("increase-quantity/<str:name>/", views.decrease_quantity, name="decrease-quantity"),
    path("decrease-quantity/<str:name>/", views.increase_quantity, name="increase-quantity"),
]

urlpatterns += htmx_patterns
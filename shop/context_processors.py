from .utils import get_cart

def get_total_cart_count(request):
    return {"total_cart_count": len(get_cart(request))}
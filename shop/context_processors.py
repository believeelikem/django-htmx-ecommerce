from .utils import get_cart, dict_cart

def get_total_cart_count(request):
    return {"total_cart_count": len(get_cart(request))}

def cart_total_amount(request):
    total = f"{get_cart_total(dict_cart(get_cart(request))):,.2f}"
    return {"cart_total": total}

def get_cart_total(cart):
    return sum(float(cart[item]["sub_total"].replace(".00","").replace(",","")) for item in cart)
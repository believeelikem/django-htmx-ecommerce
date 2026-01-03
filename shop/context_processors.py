
def get_total_cart_count(request):
    return {"total_cart_count": len(request.session["cart"] if "cart" in request.session else None)}
def get_variant(details, color, size):
    if not all([color,size]):
        return details[0]
    
    for detail in details:
        if detail["color"] == color and detail["size"] == size:
            return detail
        
    for detail in details:
        if detail["color"] == color:
            return detail
    
def get_sizes_for_chosen_color(details,color):
    sizes = []
    for detail in details:
        if detail["color"] == color:
            sizes.append(detail["size"])
    return sizes
    
def get_related_specifics(details, key):
    return list(set(detail[key] for  detail in details))

def get_product_quantity(max_quantity,product_quantity_in_session):
    should_reset = False
    if product_quantity_in_session > max_quantity:
        should_reset = True
        return max_quantity, should_reset
    return product_quantity_in_session, should_reset

def get_new_quantity(request, cart, order_item):
    increment_val = get_increment_val(request,order_item["slug"])
    
    if not cart or not is_already_in_cart(cart, order_item):
        increment_val = increment_val
    else:
        increment_val = int(request.session["cart"][order_item["slug"]]["quantity"]) + increment_val
        
    return increment_val if increment_val else "Unexpected err from add_to_cart"

def get_increment_val(request,slug):
    increment_val = 1
    if request.POST.get("from") == "detail" :
        increment_val = request.session[f"{slug}_quantity"]
    elif request.POST.get("from") == "index":
        # same as 1
        pass
    elif request.POST.get("from_cart"):
        #same as 1
        pass
    print("increment val is = ", increment_val)
    return increment_val

def get_cart_in_session(session):
    return session.setdefault("cart", {}) 
 
def get_order_item(request):
    print(request.POST.get("image_url").split("/", 2)[-1])
    
    order_item = {
        "product_id":request.POST.get("id"),
        "order":None,
        "quantity": None,
        "price":request.POST.get("price"),
        "color":request.POST.get("color"),
        "size":request.POST.get("size"),
        "price":float(request.POST.get("price")),
        "image_url": request.POST.get("image_url").split("/", 2)[-1] \
            if request.POST.get("from") == "detail" else request.POST.get("image_url"),
        "slug":request.POST.get("slug"),     
    }    
    
    
    
    return order_item
      
def is_already_in_cart(cart,order_item):    
    for item in cart:
        # print("o, r is = ",order_item)
        if cart[item]["product_id"] == order_item["product_id"] \
        and cart[item]["color"] == order_item["color"] and \
        cart[item]["size"] == order_item["size"]:
            return True
    return False
from itertools import product
import re
from .models import Order, OrderItem, Product,ProductImage, Category
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet


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

def get_new_quantity_or_err(request, cart, order_item):
    new_val = get_increment_val(request,order_item["slug"])
    
    print("is already in cart = ",is_already_in_cart(cart, order_item))
    if not cart or not is_already_in_cart(cart, order_item):
        new_val = new_val
    else:
        # works with authenticated since db data is made into dict
        print("This run")
        print("alread in cart val = ", int(cart[f'{order_item["slug"]}-{order_item["image_id"]}']["quantity"]))
        print("new val to be added is = ", new_val)
        
        new_val = (
            int(cart[f'{order_item["slug"]}-{order_item["image_id"]}']["quantity"]) + new_val 
        )
        
        print("new val after adding is = ", new_val)

    
    if new_val == 0:
        raise ValueError("Cannot go less than 0 quantity, kindly click on 'Remove' to clear") 
    
    if new_val <= int(request.POST.get("curr_total_quantity")):
        return new_val if new_val else "Unexpected err from add_to_cart"
    else:
        raise ValueError("Quantity exceed available item Quantity")

def is_already_in_cart(cart,order_item):   
    for item in cart:
        if (
            cart[item]["product_id"] == order_item["product_id"] 
            and cart[item]["color"] == order_item["color"] and 
            cart[item]["size"] == order_item["size"]
        ):
            return True
    return False

def get_increment_val(request, slug):
    increment_val = 1
    if request.POST.get("from") == "detail" :
        increment_val = request.session[f"{slug}_quantity"]
    elif request.POST.get("from") == "index":
        #same as 1
        pass
    elif request.POST.get("from_cart"):
        #same as 1
        pass
    if "subtract" == request.POST.get("action"):
        increment_val = -increment_val

    return increment_val

def get_cart_in_session(session):
    return session.setdefault("cart", {}) 

def get_cart_in_db(user):
    order = get_order(user)
    cart  = order.items.all()
    return cart

def get_order_item(request):
    
    order_item = {
        "product_id":int(request.POST.get("id")),
        "name":request.POST.get("name"),
        "order":None,
        "quantity": None,
        "price":request.POST.get("price"),
        "color":request.POST.get("color"),
        "size":request.POST.get("size"),
        "price":float(request.POST.get("price")),
        "image_url": request.POST.get("image_url"),
        "image_id": request.POST.get("image_id"),
        "slug":request.POST.get("slug"),     
        "curr_total_quantity":request.POST.get("curr_total_quantity"),
    }    
    
    return order_item
       
def get_cart(request):
    cart = None
    if request.user.is_authenticated:
        cart = get_cart_in_db(request.user)
    else:
        cart = get_cart_in_session(request.session)

    return cart 
   
def get_order(user):
    order, _ = Order.objects.get_or_create(
        owner = user, is_completed = False
    )
    return order

def dict_cart(cart):
    if not cart:
        return {}
    if isinstance(cart, QuerySet):
        dict_cart = {}
        for order_item in cart:
            dict_cart[f"{order_item.product.slug}-{order_item.image_id}"] = (
                  {
                    "product_id": order_item.product.id,
                    "name": order_item.product.name,
                    "order":order_item.order,
                    "quantity": order_item.quantity,
                    "price":get_current_val(
                        order_item.product.details, 
                        "unit_price", 
                        order_item.color,
                        order_item.size
                    ),
                    "color":order_item.color,
                    "size":order_item.size,
                    "image_url": order_item.image_url,
                    "image_id": order_item.image_id,
                    "slug":order_item.product.slug,     
                    "curr_total_quantity":get_current_val(
                        order_item.product.details, 
                        "quantity", 
                        order_item.color,
                        order_item.size
                    ),  
                    "sub_total":order_item.sub_total,
                  }
            )
        cart = dict_cart
    elif isinstance(cart, dict):
        cart = cart     
    return cart
            
def get_current_val(product_details,val,color,size):
    for variant in product_details:
        if variant["color"] == color and variant["size"] == size:
            return variant[val]
    
def get_new_count(cart,slug,image_id):
    return cart[f"{slug}-{image_id}"]["quantity"]

def merge_item(db_cart_item,session_cart_item):
    print("db cart item is = ", db_cart_item, "\n")
    print("session cart item is = ", session_cart_item, "\n")

    updated_item = {}
    
    from collections import ChainMap

    updated_item  = dict(ChainMap(db_cart_item, session_cart_item))
    print("after updated is ", updated_item)

    # updated_item =  db_cart_item | session_cart_item
    
    updated_item["quantity"] = sum([int(db_cart_item["quantity"]), int(session_cart_item["quantity"])])
    updated_item["sub_total"] = sum(
        [
            float(db_cart_item["sub_total"].replace(",","")), 
            float(session_cart_item["sub_total"].replace(",",""))
        ]
    )
    
    return updated_item


#  resistors used to do operations 
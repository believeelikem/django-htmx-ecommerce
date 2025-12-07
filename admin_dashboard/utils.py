from itertools import product
import re

from django.test import tag
from .colors import colors


def validate():
    pass

def error_processor(view_func):
    def inner(request):
        if "product_name" in request.GET:
            error_message = validate_product_name(request.GET["product_name"])
        
        elif "category_name" in request.GET:
            error_message = validate_category_name(request.GET["category_name"])
            
        elif "tag_name" in request.GET:
            error_message = validate_tag_name(request.GET["tag_name"])
            
        elif "quantity" in request.GET:
            error_message = validate_quantity(request.GET["quanrtity"])
            
        elif "size" in request.GET:
            error_message = validate_size(request.GET["size"])
            
        elif "color" in request.GET:
            error_message = validate_tag_name(request.GET["color"])
            
        elif "price" in request.GET:
            error_message = validate_tag_name(request.GET["price"])
            
        elif "product_image" in request.GET:
            error_message = validate_tag_name(request.GET["product_image"])
            
        elif "description" in request.GET:
            error_message = validate_tag_name(request.GET["description"])
         
        else:
            error_message = "Unknown error"
            
        return view_func(request, error_message = error_message)   
            
    return inner

def validate_product_name(product_name):
     
    error = ""
    
    if not product_name:
        error = "name cannot be empty"
        
    if re.search(r"\W+", product_name):
        error  = "name cannot contain non word char"
        
    if len(product_name) < 3:
        error = "name cannot be less than 3 chars"
        

    
    return error

def validate_category_name(request):
    return "Invalid also"

def validate_tag_name(tag_name):
    
    error = ""
    
    if not tag_name:
        error = "name cannot be empty"
        
    if re.search(r"\S+", tag_name):
        error = "quantity cannot contain spaces"
       
    if re.search(r"\W+", tag_name):
        error = "name cannot contain non word char"
        
    return error
    
def validate_quantity(quantity):
    
    error = ""
    if not quantity:
        error =  "quantity cannot be empty"
        
    if re.search(r"\S+", quantity):
        error = "quantity cannot contain spaces"
    
    if not quantity.isdigit():
        error = "quantity must be an integer"
        
    if int(quantity) <= 0 :
        error = "size cannot be negative"
    
    return error

def validate_size(size):
    error = ""
    if not size:
        error =  "size cannot be empty"
        
    if re.search(r"\S+", size):
        error = "size cannot contain spaces"
        
    if re.search(r"\W+", size):
        error = "size cannot contain non word char"
    
    return error

def validate_color(color):
    error = ""
    if not color:
        error =  "color cannot be empty"
        
    if re.search(r"\S+", color):
        error = "color cannot contain spaces"
 
    if re.search(r"\W+", color):
        error = "color cannot contain non word char"       
    
    if not (color.lower() in colors):
        error = "Invalid color"
    
    return error

def validate_price(price):
    error = ""
    if not price:
        error =  "price cannot be empty"
        
    if re.search(r"\S+", price):
        error = "price cannot contain spaces"
    
    if not price.isdigit():
        error = "price must be a number"
        
    if int(price) <= 0 :
        error = "size cannot be negative"
    
    return error

def validate_product_image(request):
    return "Invalid also"

def validate_description(description):
    error = ""
    if not description:
        error =  "description cannot be empty"
        
    if re.search(r"\W+", description):
        error = "description cannot contain non word char"
    
    return error

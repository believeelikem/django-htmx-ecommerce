from itertools import product
from multiprocessing import context
import re
from turtle import st
from.models import TempImage
from django.test import tag
from django.shortcuts import get_object_or_404
from .colors import colors


def validate():
    pass

def error_processor(view_func):
    def inner(request):
        error_message = ""
        css_class = ""
        if request.method == "GET":
            if "product_name" in request.GET:
                error_message = validate_product_name(request.GET["product_name"])
                css_class = "name"
            
            elif "category_name" in request.GET:
                error_message = validate_category_name(request.GET["category_name"])
                css_class = "category"
                
            elif "tag_name" in request.GET:
                error_message = validate_tag_name(request.GET["tag_name"])
                css_class = "tag"
                
            elif "quantity" in request.GET:
                error_message = validate_quantity(request.GET["quantity"])
                css_class = "quantity"
                
            elif "size" in request.GET:
                error_message = validate_size(request.GET["size"])
                css_class = "size"
                
            elif "color" in request.GET:
                error_message = validate_color(request.GET["color"])
                css_class = "color"
                
            elif "price" in request.GET:
                error_message = validate_price(request.GET["price"])
                css_class = "price"
            
                
            elif "description" in request.GET:
                error_message = validate_description(request.GET["description"])
                css_class = "description"
            
            else:
                error_message = "Unknown error"
        elif request.method == "POST":
            print("product_image in request.FILES = ","product_image" in request.FILES)
            if "product_image" in request.FILES:
                print(f"File attr is {request.FILES}")
                error_message = validate_product_image(request.FILES["product_image"])
                css_class = "image"
            
                
        return view_func(request, error_message = error_message, css_class = css_class)   
            
    return inner

def validate_product_name(product_name):
     
    error = ""
    
    if not product_name:
        error = "name cannot be empty"
            
    elif re.search(r"^\s+", product_name):
        error = "name cannot contain spaces"           
    elif re.search(r"[^\w\s-]", product_name):
        error  = "name cannot contain non word char"
    elif len(product_name) < 3:
        error = "name cannot be less than 3 chars"
        

    return error

def validate_category_name(request):
    return "Invalid also"

def validate_tag_name(tag_name):
    
    error = ""
    
    if not tag_name:
        error = "name cannot be empty"
       
    if re.search(r"\W+", tag_name):
        error = "name cannot contain non word char"

    if re.search(r"\s+", tag_name):
        error = "tag cannot contain spaces"      
    return error
    
def validate_quantity(quantity):
    print("From utils:", quantity)
    error = ""
    
    print("quantity is None",quantity is None)
    print('quantity.strip() == ""',quantity.strip() == "")
    print('bool(re.search(r"\s+", quantity))',bool(re.search(r"\s+", quantity)))
    print('quantity.isdigit()',not quantity.isdigit())
    # print('int(quantity) <= 0',int(quantity) <= 0)

    if quantity is None or quantity.strip() == "":
        error = "quantity cannot be empty"
    
    elif re.search(r"^\s+", quantity):
        error = "quantity cannot contain spaces"
    
    elif not quantity.strip().isdigit():
        error = "quantity must be a positive integer"
    
    elif int(quantity) <= 0:
        error =  "quantity must be greater than zero"
        
    return error
    
    
def validate_size(size):
    error = ""
    if not size:
        error =  "size cannot be empty"
        
    elif re.search(r"^\s+", size):
        error = "size cannot contain spaces"
        
    elif re.search(f"[^\\w\\s]", size):
        error = "size cannot contain non word char"
    
    return error


def validate_color(color):
    error = ""
    
    if not color:
        error =  "color cannot be empty"
        
    elif re.search(r"\s+", color):
        error = "color cannot contain spaces"
 
    elif re.search(r"\W+", color):
        error = "color cannot contain non word char"       
    
    elif not (color.lower() in colors):
        error = "Invalid color"
    
    return error

def validate_price(price):
    print("price is ", price)
    error = ""
    if not price:
        error =  "price cannot be empty"
        
    elif re.search(r"\s+", price):
        error = "price cannot contain spaces"

    elif classify_number_value(price.strip()) == 'Not a number':
        error = "price must be positive integer or float"
    
    elif classify_number_value(price.strip()) == "Float":
        if len(price.strip().split(".")[1]) > 2:
            error = "Cannot enter more than 2 decimal places"
   
    #     error = "price must not be negative"   
    # elif int(price) <= 0 :
    #     error = "size cannot be negative"
    
    return error

def validate_product_image(image_object):
    error = ""
    if len(image_object.name.split('.')[0]) > 25:
        print(image_object.name.split('.')[0])
        error = "image name too long"
    elif not is_valid_image_extension(image_object.name):
        error = f".{image_object.name.split('.')[1]} is invalid, choose .jpg,.jpeg,.png"
    return error

def is_valid_image_extension(name):
    if name.endswith((".jpeg", ".png",".jpg")):
        return True
    return False

def validate_description(description):
    error = ""
    if not description or description.strip() == "":
        error =  "description cannot be empty"

    return error


def is_string_integer(s):
    
    try:
        int(s)
        return True
    except ValueError:
        return False

def classify_number_value(s):
    """
    Classifies a string's numeric value as 'Integer', 'Float', or 'Not a number'.
    Treats values like '10.0' as 'Integer'.
    """
    try:
        num = float(s)
        if num < 0:
            raise ValueError()
        if num.is_integer():
            return 'Integer'
        else:
            return 'Float'
        
    except ValueError:
        return 'Not a number'




def add_to_list_session_handler(view_func):
    def wrapper(request):
        temp_image = TempImage(temp_image = request.FILES["product_image"])
        temp_image.save()
        product_details = []
        if "product_details" not in request.session:
            print("Product details in session")
            product_details = request.session["product_details"] = product_details
            
        else:
            product_details = request.session["product_details"]
        
            
        product_details.append(
            {
                "product_id": get_id(product_details),
                "product_image_id":temp_image.id,
                "product_name":request.POST["product_name"],
                "category_name": request.POST["category_name"],
                "tag_name":request.POST["tag_name"],
                "is_digital":request.POST["is_digital"],
                "quantity":request.POST["quantity"],
                "size":request.POST["size"],
                "color":request.POST["color"],
                "price":request.POST["price"],
                "description":request.POST["description"]
            }
        )
        
        request.session["product_details"] = product_details
       
        
        context = {
            "product_details": product_details.copy(),
        }
        
        return view_func(request, context = context)
    return wrapper


def attach_product_images(context):
    for product in context["product_details"]:
        product["total_price"] = f"{float(product['price']) * float(product['quantity']):,.2f}"
        try:
            product["image_url"] = get_object_or_404(TempImage, id = product["product_image_id"]).temp_image.url
        except TempImage.DoesNotExist as e:
            print("Didnt find image")
            print(e)
    return context


def get_table_total_price(product_details):
    total = 0
    for product in product_details:
        total += float(product["total_price"].replace(",",""))
    return total


def get_id(session_data):
    current_max = get_max_id(session_data)
    print("current max is ", current_max)
    return current_max + 1

    
def get_max_id(session_data):
    ids = []
    return max([product["product_id"] for product in session_data ], default=0)

    # if session_data:
    #     for product in session_data:
    #         ids.append(product["product_id"])
    # else:
    #     ids.append(1)
        
    # return max(ids)
    
# def attach session data
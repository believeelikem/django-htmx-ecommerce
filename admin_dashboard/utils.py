from unicodedata import category
from.models import TempImage
from django.shortcuts import get_object_or_404
from .colors import colors
from shop.models import  Product, ProductImage, Category
from django.core.files.base import ContentFile
import os
import re


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
                print("Hit here at 1:34")
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
            if "product_image" in request.FILES:
                error_message = validate_product_image(request.FILES["product_image"])
                
                    
            if request.POST.get("product_id",""):
                error_message = {
                    "error_message":error_message,
                    "product_id":request.POST.get("product_id"),
                    "new_image_chosen": True if "product_image" in request.FILES else False
                }
                      
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


def add_product_to_list_session_handler(images_wrapper_func):
    def product_details_wrapper(request):
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
                "is_digital":request.POST.get("is_digital", "off"),
                "quantity":request.POST["quantity"],
                "size":request.POST["size"],
                "color":request.POST["color"],
                "price":request.POST["price"],
                "description":request.POST["description"],
                "is_being_edited":False
            }
        )
        
        request.session["product_details"] = product_details

        return images_wrapper_func(request)
    
    return product_details_wrapper


def attach_product_images(view_func):
    def attach_images_wrapper(request,id = None):
        context = {}
        if "product_details" in request.session:
            context = {"product_details": request.session["product_details"] .copy()}
            for product in context["product_details"]:
                product["total_price"] = f"{float(product['price']) * float(product['quantity']):,.2f}"
                
                try:
                    product["image_url"] = get_object_or_404(TempImage, id = \
                    product["product_image_id"]).temp_image.url
                    
                except TempImage.DoesNotExist as e:
                    print("Didnt find image")
                    print(e)
            
            context["total_price"] = f"{get_table_total_price(context['product_details']):,.2f} "
        
        if request.method == "DELETE":
            return view_func(request,id = id, context = context)
       
        return view_func(request, context)
    return attach_images_wrapper


def get_table_total_price(product_details):
    total = 0
    for product in product_details:
        total += float(product["total_price"].replace(",",""))
    return total


def get_id(session_data):
    return _get_max_id(session_data) + 1
    
def _get_max_id(session_data):
    return max([product["product_id"] for product in session_data ], default=0)
    
def get_product(request,id):
    for product in request.session["product_details"]:        
        if product["product_id"] == id:
            return product
    return None

def refix_editing_status(request):
    for _product in request.session["product_details"]:
        if  _product["is_being_edited"]:
            _product["is_being_edited"] = False
            request.session.modified = True
        
def get_product_already_being_edited(request, new_product):
    product_already_being_edited = None
    for _product in request.session["product_details"]:
        if  _product != new_product  and  _product["is_being_edited"]:
            _product["is_being_edited"] = False
            request.session.modified = True
            product_already_being_edited = _product
            break
    return product_already_being_edited 

def set_product_editing_status(request,product):
        index = request.session["product_details"].index(product)
        product["is_being_edited"] = True
        request.session["product_details"][index] = product
        request.session.modified = True
        
        return product


def product_update_in_list(images_wrapper_func):
    def product_update_details_wrapper(request):
        to_be_edited_product_id = request.POST.get("product_id")
     
        if to_be_edited_product_id:
            to_be_edited_product = get_product(request, int(to_be_edited_product_id))
            
            image_id = None
            
            if "product_image" in request.FILES:               
                temp_image = TempImage(temp_image = request.FILES["product_image"])    
                temp_image.save()
                image_id = temp_image.id  
                                             
            else:
                image_id = to_be_edited_product["product_image_id"]
                                             
            new_product_details = {
                
                    "product_id": to_be_edited_product["product_id"],
                    "product_image_id":image_id,
                    "product_name":request.POST["product_name"],
                    "category_name": request.POST["category_name"],
                    "tag_name":request.POST["tag_name"],
                    "is_digital":request.POST.get("is_digital", "off"),
                    "quantity":request.POST["quantity"],
                    "size":request.POST["size"],
                    "color":request.POST["color"],
                    "price":request.POST["price"],
                    "description":request.POST["description"],
                    "is_being_edited":False
                
            }
            
            to_be_edited_product_index = request.session["product_details"].index(
                to_be_edited_product
            )
            request.session["product_details"][to_be_edited_product_index] = new_product_details
            request.session.modified = True
            
            return images_wrapper_func(request)
        else:
            print("Theres no id")
        
    return product_update_details_wrapper
           
def save_to_db(view_func):
    def save_to_db_wrapper(request):
        
        grouped_products = group_products(request.session["product_details"])
        
        # loop through grouped items 
        for _product_name in grouped_products:
            product = Product.objects.create(name = _product_name)
            quantity = 1
            
            
            # loop through details of an item to save to db
            for _product_detail in grouped_products[_product_name]:
                quantity *= float(_product_detail["quantity"])
                
                #get temporary image of product
                _product_detail_temp_image = get_object_or_404(
                    TempImage, id = _product_detail["product_image_id"]
                )
                
                # create actual product obj and assign temp image 
                _product_detail_product_image = ProductImage()
                
                # extract basename of tempimage to use as name for new product to be added to db
                _product_detail_temp_image_basename = os.path.basename(
                    _product_detail_temp_image.temp_image.path
                )
                
                # extract the bytes of the image and save it to new product
                _product_detail_product_image.photo.save(
                    _product_detail_temp_image_basename, 
                    ContentFile(
                        _product_detail_temp_image.temp_image.read()
                    ),
                    save= False
                )
                
                # save new product image early so it can be linked to product
                _product_detail_product_image.product = product
                _product_detail_product_image.save()
                
                # append other details to the product
                product.details.append(
                    {
                     'tag_name': _product_detail["tag_name"], 
                     'is_digital': _product_detail["is_digital"], 
                     'quantity': _product_detail["quantity"], 
                     'size': _product_detail["size"], 
                     'color': _product_detail["color"], 
                     'unit_price': _product_detail["price"], 
                     'description': _product_detail["description"] ,
                     'image_id':_product_detail_product_image.id,
                     'total_price': float(_product_detail["total_price"].replace(",",""))
                    }
                )
                
                
                _product_detail_temp_image.temp_image.delete(save=False)
                _product_detail_temp_image.delete()
            
                
            product.category.add(
                get_object_or_404(Category,
                                  name = grouped_products[_product_name][0]["category_name"]
                        )
            )
            product.is_digital = True if   grouped_products[_product_name][0]["is_digital"] \
                == "on" else False
            product.quantity = quantity
            product.save()
                
        
        return view_func(request)
    return save_to_db_wrapper
    
def group_products(product_data):
    grouped_products = {}
    
    for _product in product_data:
        grouped_products.setdefault(_product["product_name"], []).append(_product)        
    return grouped_products


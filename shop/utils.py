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

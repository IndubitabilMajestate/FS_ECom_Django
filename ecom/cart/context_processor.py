from .cart import Cart

def cart(request):
    #Return the data from the Cart
    return {'cart': Cart(request)}

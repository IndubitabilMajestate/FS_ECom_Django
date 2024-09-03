from store.models import Product
class Cart():
    def __init__(self, request):
        self.session = request.session
        
        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            cart = self.session["session_key"] = {}
        
        self.cart = cart
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        cart = self.cart
        cart[product_id] = product_qty
        
        self.session.modified = True
        return self.cart

    def delete(self,product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True
        return self.cart
    
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        cart_total = 0
        for id, quantity in quantities.items():
            id = int(id)
            for product in products:
                if product.id == id:
                    if product.on_sale:
                        cart_total = cart_total+product.sale_price*quantity
                    else:
                        cart_total = cart_total+product.price*quantity
        return cart_total
        

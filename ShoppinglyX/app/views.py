from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced
from django.db import models
from .forms import UserRegistrationForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import *


#def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category = 'TW')
        bottom_wear = Product.objects.filter(category = 'BW') 
        mobiles = Product.objects.filter(category = 'M')
        context = {'top_wears':topwears, 'bottom_wears':bottom_wear, 'mobiles':mobiles}
        return render(request, 'app/home.html', context)   
#def product_detail(request):
# return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        is_item_in_cart = False
        if(request.user.is_authenticated):
            is_item_in_cart = Cart.objects.filter(Q(product = product.id) & Q(user= request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product, 'is_item_in_cart' : is_item_in_cart})
    
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user = user, product = product).save()
    return redirect('/cart')
@login_required(login_url='login')
def show_cart(request):
    if(request.user.is_authenticated):
        user =  request.user
        cart_item = Cart.objects.filter(user =user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        item_count = 0
        if cart_product:
            for p in cart_product:
                temp_amount = p.quantity * p.product.discounted_price
                amount += temp_amount
                item_count += 1
            total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'cart_item': cart_item, 'total_amount' : total_amount, 'shipping_amount' : shipping_amount, 'amount' : amount, 'item_count' : item_count})
        else:return render(request, 'app/empty_cart.html', {'item_count' : item_count})

def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product = prod_id) & Q(user = user))
        cart.quantity += 1
        cart.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount
        total_amount = amount + shipping_amount
        data = {'total_amount' : total_amount, 'amount' : amount, 'quantity' : cart.quantity}
        
        return JsonResponse(data)
        

def minus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product = prod_id) & Q(user = user))
        cart.quantity -= 1
        cart.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount
        total_amount = amount + shipping_amount
        data = {'total_amount' : total_amount, 'amount' : amount, 'quantity' : cart.quantity}
        
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product = prod_id) & Q(user = user))
        cart.quantity -= 1
        cart.delete()
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount
        if amount>0:
            shipping_amount = 70.0
        total_amount = amount + shipping_amount
        data = {'total_amount' : total_amount, 'amount' : amount, 'shipping_amount': shipping_amount}
        
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

#def profile(request):
 #return render(request, 'app/profile.html')

class ProfileView(View):
    def get(self,request):
        forms = CustomerRegistrationForm()
        return render(request, 'app/profile.html', {'form': forms})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user = user, name = name, locality = locality, city = city, state = state, zipcode = zipcode)
            reg.save()
            messages.success(request, ' Congratulations !! Profile Updated Successfully! ')
        return render(request, 'app/profile.html', {'form': form, 'active':'btn-primary'})
    

def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', {'add': add, 'active':'btn-primary'})

@login_required
def orders(request):
    ordered = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html', {'ordered' : ordered})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data = None):
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'sumsung' or data == 'redmi':
        mobiles = Product.objects.filter(category = 'M').filter(brand = data)
    elif data == 'below':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt = 10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt = 10000)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def login(request):
 return render(request, 'app/login.html')


#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations Registered Succesfully!!')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})
            
        

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_item = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 0.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            temp_amount = p.quantity * p.product.discounted_price
            amount += temp_amount
        if amount >0:
            shipping_amount = 70.0
        total_amount = shipping_amount + amount
    return render(request, 'app/checkout.html', {'add': add, 'cart_item': cart_item, 'total_amount' : total_amount})


def payment_done(request):
    user = request.user
    cust_id = request.GET.get('custid')
    if cust_id:
        print(cust_id)
    else:
        print('nothing')
    customer = Customer.objects.get(id = cust_id)
    cart = Cart.objects.filter(user = user)
    for item in cart:
        OrderPlaced(user = user, customer = customer, product = item.product, quantity = item.quantity).save()
        item.delete()
    return redirect("orders")


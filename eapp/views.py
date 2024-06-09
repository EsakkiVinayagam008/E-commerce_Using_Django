import json
from django.shortcuts import redirect, render
from django.http import  JsonResponse
from eapp.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

# Create your views here.
def index(request):
    product1=Product.objects.filter(trending=1)
    
    return render(request,'index.html',{"product1":product1})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('index')
            else:
                messages.error(request,"Invalid  User Name or Password")
                return redirect('/login')  
        
        return render(request,'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Success...")
    return redirect('index')
    

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registered Successfully...")
            return redirect('/login')
    return render(request,'register.html',{"form":form})

def add_to_cart(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product already in cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product added in cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Avalible'},status=200)
                        
                    
            return JsonResponse({'status':'Product Added'},status=200)
        else:
            return JsonResponse({'status':'Login before Add to Cart'},status=200)
            
    else:
        return JsonResponse({'status':'invalid access'},status=200)



def product(request):
    catagory=Catagory1.objects.filter(status=0)
    return render(request,'product.html',{"catagory":catagory})

def productview(request,name):
    if(Catagory1.objects.filter(status=0)):
        product1=Product.objects.filter(category__name=name)
        return render(request,'productlist.html',{"product1":product1,"catagory_name":name})
    else:
        messages.warning(request,"Not such categarys found")
        return redirect('product')
    
def product_details(request,cname,pname):
    if(Catagory1.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            product1=Product.objects.filter(name=pname,status=0).first()
            return render(request,'product_details.html',{"product1":product1})
        else:
            messages.error(request,"Not such categarys found")
            return redirect('product')
    else:
        messages.error(request,"Not such categarys found")
        return redirect('product')
            
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'cart.html',{'cart':cart})
    else:
        return redirect('/')
    
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')

def buy_now(request):
    if request.user.is_authenticated:
        return render(request, 'buynow.html')
    else:
        return redirect('login')
    
        
        
    
        
    
            
    
        
    
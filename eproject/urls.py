"""
URL configuration for eproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from eapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('cart',views.cart_page,name='cart'),
    path('removecart/<str:cid>',views.remove_cart,name='removecart'),
    path('product',views.product,name='product'),
    path('product/<str:name>',views.productview,name='product'),
    path('product/<str:cname>/<str:pname>',views.product_details,name='product_details'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('buynow',views.buy_now,name='buynow'),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    

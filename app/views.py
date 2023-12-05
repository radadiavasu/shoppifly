from django.db import models
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets

from app.serializers import CustomerSerializer
from rest_framework.views import APIView
# from rest_framework.response import Response
# from app.serializers import CustomerSerializer
from .models import Cart, Customer, OrderPlaced, Product, Contact, Rating
from app.forms import ContactForm, CustomerRegistratiopnForm, LoginForm, ProfileForm, RatingForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.template.loader import render_to_string


def page_not_found(request, exception):
    return render(request, 'app/404.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    already_add = False
    if request.user.is_authenticated:
        if product.cartitem_set.filter(cart__user=request.user).exists():
            already_add = True
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            Rating.objects.create(user=request.user, product=product, rating=rating)
            return redirect('productdetail', product_id=product_id)
    else:
        form = RatingForm()
    context = {
        'product': product,
        'already_add': already_add,
        'form': form
    }
    return render(request, 'app/productdetail.html', context)

def MailContact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = Contact()
            data.fullname = form.cleaned_data['fullname']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.phone_number = form.cleaned_data['phone_number']
            data.message = form.cleaned_data['message']
            data.save()
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            fullname = form.cleaned_data['fullname']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['vasuradadia850@gmail.com',]
            html_message = loader.render_to_string(
                'email.html',
                {
                    'subject':subject,
                    'message':message,
                    'fullname':fullname,
                    'email':email,
                    'phone_number':phone_number,
                }
            )
            if subject and message and email_from and recipient_list and html_message:
                try:
                    send_mail(subject, message, email_from, recipient_list, html_message = html_message, fail_silently=False)
                except:
                    messages.error(request,"Cannot send mail right now, Try again later")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                messages.success(request,"Message sent successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"Please! Make sure all fields are entered and valid.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,"Please! Make sure all fields are entered and valid.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    return render(request, 'app/contact.html')

class ProductView(View):
    def get(self, request):
        total_items = 0
        top_wear = Product.objects.filter(category__name="TopWears")
        bottom_wear = Product.objects.filter(category__name="BottomWears")
        mobile = Product.objects.filter(category__name="Mobiles")
        laptop = Product.objects.filter(category__name="Laptops")
        shoes = Product.objects.filter(category__name="Shoes")
        watch = Product.objects.filter(category__name="Watch")
        trending = OrderPlaced.objects.order_by('?')

        if len(trending) < 5:
            pass
        else:
            trending = trending[:5]

        print(trending)
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'top_wear': top_wear, 'bottom_wear': bottom_wear, 'mobile': mobile, 'laptop': laptop, 'shoes': shoes, 'watch': watch,'trending': trending, 'total_items': total_items})


class ProductDetailView(View):
    def get(self, request, id):
        total_items = 0
        product = Product.objects.get(id=id)
        already_add = False
        if request.user.is_authenticated:
            already_add = Cart.objects.filter(
                user=request.user, product=product).exists()
            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product': product, 'already_add': already_add, 'total_items': total_items})


def mobile(request, data=None):
    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    if data == None:
        mobiles = Product.objects.filter(category__name="Mobiles")
    elif data == "below":
        mobiles = Product.objects.filter(
            category__name="Mobiles").filter(discounted_price__lt=242)
    elif data == "above":
        mobiles = Product.objects.filter(
            category__name="Mobiles").filter(discounted_price__gte=242)
    else:
        mobiles = Product.objects.filter(
            category__name="Mobiles").filter(brand=data)
    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'total_items': total_items})
    

def laptop(request, data=None):

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    if data == None:
        laptops = Product.objects.filter(category__name="Laptops")
    elif data == 'below':
        laptops = Product.objects.filter(
            category__name="Laptops").filter(discounted_price__lt=728)
    elif data == 'above':
        laptops = Product.objects.filter(
            category__name="Laptops").filter(discounted_price__gte=728)
    else:
        laptops = Product.objects.filter(
            category__name="Laptops").filter(brand=data)

    return render(request, 'app/laptop.html', {'laptops': laptops, 'total_items': total_items})


def topwear(request):

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    topwears = Product.objects.filter(category__name="TopWears")
    return render(request, 'app/topwear.html', {'topwears': topwears, 'total_items': total_items})


def bottomwear(request):

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    bottomwears = Product.objects.filter(category__name="BottomWears")
    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears, 'total_items': total_items})


def shoes(request):

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))
        
    shoes = Product.objects.filter(category__name="Shoes")
    return render(request, 'app/shoes.html', {'shoes': shoes, 'total_items': total_items})


def watch(request):

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    watch = Product.objects.filter(category__name="Watch")
    return render(request, 'app/watch.html', {'watch': watch, 'total_items': total_items})


@ method_decorator(login_required, name="dispatch")
class ProfileView(View):
    total_items = 0

    def get(self, request):
        fm = ProfileForm()
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': fm,  'total_items': total_items})

    def post(self, request):

        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))

        fm = ProfileForm(request.POST)
        if fm.is_valid():
            user = request.user
            name = fm.cleaned_data['name']
            locality = fm.cleaned_data['locality']
            city = fm.cleaned_data['city']
            zipcode = fm.cleaned_data['zipcode']
            state = fm.cleaned_data['state']
            obj = Customer(user=user, name=name, locality=locality,
                           city=city, zipcode=zipcode, state=state)
            obj.save()
            messages.success(request, 'Address has been successfully added!!!')
            return HttpResponseRedirect('/address/')
        return render(request, 'app/profile.html', {'form': fm, 'total_items': total_items})


@ login_required
def address(request):

    customers = Customer.objects.filter(user=request.user)

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/address.html', {'customers': customers, 'total_items': total_items})


@ method_decorator(login_required, name="dispatch")
class EditAddressView(View):

    def get(self, request, id):
        instance = Customer.objects.get(id=id)
        fm = ProfileForm(instance=instance)
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/edit_profile.html', {'form': fm, 'total_items': total_items})

    def post(self, request, id):
        instance = Customer.objects.get(id=id)
        fm = ProfileForm(request.POST, instance=instance)
        if fm.is_valid():
            fm.save()
            return redirect("/address/")


@ method_decorator(login_required, name="dispatch")
class DeleteAddressView(View):
    def get(self, request, id):
        instance = Customer.objects.get(id=id)
        instance.delete()
        return redirect("/address/")


@ login_required
def add_to_cart(request):
    try:
        prod_id = request.GET['prod_id']
    except:
        return redirect('/')
    user = request.user
    product = Product.objects.get(id=prod_id)
    Cart(user=user, product=product).save()
    return redirect("/")


@ login_required
def show_cart(request):
    user = request.user
    carts = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 1.82
    total_amount = 0.0

    cart_product = [p for p in Cart.objects.filter(user=user)]
    if cart_product:
        for p in cart_product:
            each_amount = (p.quantity * p.product.discounted_price)
            amount += each_amount
        total_amount = amount + shipping_amount

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/addtocart.html', {'carts': carts, 'amount': amount, 'total_amount': total_amount, 'shipping_amount': shipping_amount, 'total_items': total_items})


@ login_required 
def plus_cart(request):
    if request.method == "GET":
        try:
            id = request.GET['product_id']
        except:
            return redirect('/')
        cart = Cart.objects.get(product=id, user=request.user)
        cart.quantity += 1
        cart.save()

        amount = 0.0
        shipping_amount = 1.82
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for p in cart_product:
                each_amount = (p.quantity * p.product.discounted_price)
                amount += each_amount
            total_amount = amount + shipping_amount

        data = {
            'quantity': cart.quantity,
            'amount': amount,
            'total_amount': total_amount
        }
    return JsonResponse(data)


@ login_required 
def minus_cart(request):
    if request.method == "GET":
        try:
            id = request.GET['product_id']
        except:
            return redirect('/')

        cart = Cart.objects.get(product=id, user=request.user)
        if(cart.quantity > 1):
            cart.quantity -= 1
        else:
            cart.quantity = 1
        cart.save()

        amount = 0.0
        shipping_amount = 1.82
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for p in cart_product:
                each_amount = (p.quantity * p.product.discounted_price)
                amount += each_amount
            total_amount = amount + shipping_amount

        data = {
            'quantity': cart.quantity,
            'amount': amount,
            'total_amount': total_amount
        }
    return JsonResponse(data)


@ login_required
def remove_cart(request):
    if request.method == "GET":

        try:
            id = request.GET['product_id']
        except:
            return redirect('/')

        cart = Cart.objects.get(product=id, user=request.user)
        cart.delete()

        amount = 0.0
        shipping_amount = 1.82
        total_amount = 0.0

        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for p in cart_product:
                each_amount = (p.quantity * p.product.discounted_price)
                amount += each_amount
            total_amount = amount + shipping_amount

        data = {
            'amount': amount,
            'total_amount': total_amount
        }
    return JsonResponse(data)


@ login_required
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 1.82
    total_amount = 0.0

    cart_product = [p for p in Cart.objects.filter(user=request.user)]
    if cart_product:
        for p in cart_product:
            each_amount = (p.quantity * p.product.discounted_price)
            amount += each_amount
        total_amount = amount + shipping_amount

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/checkout.html', {'user': user, 'addresses': address, 'cart_items': cart_items, 'amount': amount, 'total_amount': total_amount, 'shipping_amount': shipping_amount, 'total_items': total_items})


@ login_required
def orderdone(request):
    user = request.user
    cust = Customer.objects.filter(user=user).exists()

    if cust:
        try:
            custid = request.GET['custid']
        except:
            return redirect("/checkout")
    else:
        return redirect("/profile")

    customer = Customer.objects.get(id=custid)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        OrderPlaced(user=user, customer=customer,
                    product=cart.product, quantity=cart.quantity, status="Accepted").save()
        cart.delete()
    return redirect('/orders')


@ login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)

    total_items = 0
    if request.user.is_authenticated:
        total_items = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/orders.html', {'order_placed': op, 'total_items': total_items})


def buy_now(request):
    return render(request, 'app/buynow.html')

# class CustomerRegistrationAPI(APIView):
#     def post(self, request):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "User has been registered successfully!!!"
#             })
#         return Response(serializer.errors)

class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRegistrationView(View):
    def get(self, request):

        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))

        fm = CustomerRegistratiopnForm()

        return render(request, 'app/customerregistration.html', {'form': fm, 'total_items': total_items})

    def post(self, request):

        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))

        fm = CustomerRegistratiopnForm(request.POST)
        if fm.is_valid():
            serializer = CustomerSerializer(data=fm.cleaned_data)
            if serializer.is_valid():
                serializer.save()
            messages.success(
                request, 'User has been registered successfully!!!')
            fm.save()
            return HttpResponseRedirect('/accounts/login/')
        return render(request, 'app/customerregistration.html', {'form': fm, 'total_items': total_items})


class LoginView(View):

    def get(self, request):
        fm = LoginForm()

        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/login.html', {'form': fm, 'total_items': total_items})

    def post(self, request):

        total_items = 0
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))

        fm = LoginForm(request, request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                messages.success(request, "You have successfully logged in!!!")
                login(request, user)
                return HttpResponseRedirect("/")
        return render(request, 'app/login.html', {'form': fm, 'total_items': total_items})


@ login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')
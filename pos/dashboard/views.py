from django.shortcuts import render, redirect, get_object_or_404
from . models import Product, Cart, Order
from . forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def dashboard(request):
    maincourser_product = Product.objects.filter(category='MC')
    appetizers_product = Product.objects.filter(category='Ap')
    drinks_product = Product.objects.filter(category='Dr')
    orders= Order.objects.all()
    if request.user.is_staff and request.user.is_superuser:
      workers = User.objects.all()
      worker_count = workers.count()
      orders = Order.objects.all()
      orders_count = orders.count()
      context={
        'orders':orders,
        'worker_count': worker_count,
        'orders_count': orders_count
      }
      return render(request, 'dashboard/admin_index.html', context)
    
    else:
      user= User.objects.get(username=request.user)
      cart_count = Cart.objects.filter(user=user).count()
      order_count = Order.objects.filter(staff=user).count()
      context ={
          'maincourser_product':maincourser_product,
          'appetizers_product':appetizers_product,
          'drinks_product':drinks_product,
          'order_count':order_count,
          'cart_count': cart_count,
      }
      return render(request, 'dashboard/index.html', context)
    
# All Order by staff
@login_required 
def All_Order(request):
  workers = User.objects.all()
  worker_count = workers.count()
  orders = Order.objects.all()
  orders_count = orders.count()

  context={
    'orders':orders,
    'worker_count': worker_count,
    'orders_count': orders_count,
  }
  return render(request, 'dashboard/order.html', context)

# All staff 
@login_required
def Staff(request):
    workers = User.objects.all()
    worker_count = workers.count()
    orders = Order.objects.all()
    orders_count = orders.count()
    context = {
        'workers': workers,
        'worker_count': worker_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/staff.html', context)

# staff details
@login_required
def staff_detail(request , pk):
    workers = User.objects.get(id=pk)
    context ={
        'workers': workers
    }
    return render(request, 'dashboard/staff_detail.html', context)

# Profile
@login_required
def Profile(request):
    return render(request, 'user_account/profile.html')

# Prfile Update
@login_required
def Profile_update(request):
    if request.method =='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
            print('update')
    else:
        user_form = UserUpdateForm( instance=request.user)
        profile_form = ProfileUpdateForm( instance=request.user.profile)

    context={
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user_account/profile_update.html', context)


# Add to Cart
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/dashboard')


# Show cart
@login_required
def show_cart(request):
    user= User.objects.get(username=request.user)
    cart_count = Cart.objects.filter(user=user).count()
    order_count = Order.objects.filter(staff=user).count()
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount 
    else:
      context={
        'order_count':order_count,
        'cart_count': cart_count,
      }
      return render(request,'dashboard/emptycart.html', context)
    return render(request, 'dashboard/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount,'order_count':order_count, 'cart_count': cart_count})
  
# Plus Cart
@login_required
def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity +=1
    c.save()
    amount = 0.0
    shipping_amount = 100.0
    cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data ={
      'quantity' : c.quantity,
      'amount' : amount,
      'totalamount' : amount + shipping_amount
    }
    return JsonResponse(data)

# Minus Cart
@login_required
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity -=1
    c.save()
    amount = 0.0
    shipping_amount = 100.0
    cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data ={
      'quantity' : c.quantity,
      'amount' : amount,
      'totalamount' : amount + shipping_amount
    }
    return JsonResponse(data)
  
# Remove cart
@login_required
def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 100.0
    cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      totalamount = amount + shipping_amount

    data ={
      'amount' : amount,
      'totalamount' : totalamount + shipping_amount
    }
    return JsonResponse(data)

# payment_done
@login_required
def payment_done(request):
  user = request.user
  cart = Cart.objects.filter(user=user)
  for c in cart:
    Order(staff=user,  product = c.product, order_quantity=c.quantity).save()
    c.delete()
  return HttpResponseRedirect('/cart/')

# Staff order
@login_required
def staff_order(request):
  user= User.objects.get(username=request.user)
  orders= Order.objects.filter(staff=user)
  cart_count = Cart.objects.filter(user=user).count()
  order_count = Order.objects.filter(staff=user).count()
  context={
    'orders':orders,
    'order_count':order_count,
    'cart_count': cart_count,
  }
  return render(request, 'dashboard/staff_order.html', context)

# Sign Up
def SignUp(request):
  if not request.user.is_authenticated:
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form =RegisterForm()
    context={
        'form':form
    }
    return render(request, 'user_account/register.html', context)
  else:
     return HttpResponseRedirect('/dashboard/')

# Login
def Login(request):
  if not request.user.is_authenticated:
    if request.method=='POST':
        form=AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            urname=form.cleaned_data['username']
            urpass=form.cleaned_data['password']
            user=authenticate(username=urname, password=urpass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
    else:
        form=AuthenticationForm()
    context={
        'form':form
    }
    return render(request, 'user_account/login.html', context)
  else:
     return HttpResponseRedirect('/dashboard/')

# Logout
@login_required
def Logout(request):
    logout(request)
    return redirect('/')
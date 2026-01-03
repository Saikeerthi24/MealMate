from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
import uuid
from .models import Item, Restaurant, User, Cart, Order

# Create your views here.
def index(request):
    return render(request, "index.html")
def open_signin(request):
    return render(request, 'signin.html')

def open_signup(request):
    return render(request, 'signup.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if User.objects.filter(username=username).exists():
            return HttpResponse("This username is already registered. Please use a different email.")

        user = User(username=username, password=password, email=email, mobile=mobile, address=address)
        user.save()
        #return HttpResponse("Sign up Successful")
        #return HttpResponse(f"Username : {username} password : {password} email {email} mobile {mobile} address {address}")
        return render(request, "signin.html") 

    else:
        return HttpResponse("Invalid Response")
    
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(username, password)

    try:
        User.objects.get(username = username, password = password)
        if username == 'admin':
            return render(request, 'admin_home.html')
        else:
            restaurantList = Restaurant.objects.all()
            return render(request, 'customer_home.html',{"restaurantList" : restaurantList, "username" : username})

    except User.DoesNotExist:
        return render(request, 'fail.html')
def open_add_restaurant(request):
    return render(request, 'add_restaurant.html')
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("Duplicate restaurant!")
            
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
            )
        return HttpResponse("Successfully Added !")
        return render(request, 'admin_home.html')
def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})
def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant" : restaurant})
def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})
def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})
def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    #return render(request, 'admin_home.html')
    return HttpResponse("Item added successfully!")
def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    #return HttpResponse("Items collected")
    return render(request, 'customer_menu.html'
                  ,{"itemList" : itemList,
                     "restaurant" : restaurant, 
                     "username":username})
def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    restaurant_id = item.restaurant.id
    item.delete()
    return redirect('open_update_menu', restaurant_id=restaurant_id)
def add_to_cart(request, item_id, username):
    item = Item.objects.get(id = item_id)
    customer = User.objects.get(username = username)
    cart, created = Cart.objects.get_or_create(customer = customer)
    cart.items.add(item)
    return HttpResponse('added to cart')

def remove_from_cart(request, item_id, username):
    item = Item.objects.get(id=item_id)
    customer = User.objects.get(username=username)
    cart = Cart.objects.filter(customer=customer).first()
    if cart:
        cart.items.remove(item)
    return redirect('show_cart', username=username)
def show_cart(request, username):
    customer = User.objects.get(username = username)
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0


    return render(request, 'cart.html',{"itemList" : items, "total_price" : total_price, "username":username})

def initiate_payment(request, username):
    if request.method == 'POST':
        try:
            customer = User.objects.get(username=username)
            cart = Cart.objects.filter(customer=customer).first()
            
            if not cart or cart.items.count() == 0:
                return JsonResponse({'error': 'Cart is empty'}, status=400)
            
            total_amount = cart.total_price()
            amount_in_paise = int(total_amount * 100)  # Convert to paise
            
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Create Razorpay order
            razorpay_order = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': '1'
            })
            
            # Create order in database
            order_id = f"ORD_{uuid.uuid4().hex[:10].upper()}"
            order = Order.objects.create(
                customer=customer,
                order_id=order_id,
                razorpay_order_id=razorpay_order['id'],
                amount=total_amount,
                status='PENDING'
            )
            
            # Add items to order
            for item in cart.items.all():
                order.items.add(item)
            
            return JsonResponse({
                'order_id': order_id,
                'razorpay_order_id': razorpay_order['id'],
                'amount': amount_in_paise,
                'currency': 'INR',
                'key': settings.RAZORPAY_KEY_ID,
                'name': 'MealMate',
                'description': 'Food Order Payment',
                'prefill': {
                    'name': customer.username,
                    'email': customer.email,
                    'contact': customer.mobile
                }
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')
            
            # Verify payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            # Verify signature
            try:
                client.utility.verify_payment_signature(params_dict)
                
                # Update order status
                order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                order.razorpay_payment_id = razorpay_payment_id
                order.razorpay_signature = razorpay_signature
                order.status = 'PAID'
                order.save()
                
                # Clear cart after successful payment
                cart = Cart.objects.filter(customer=order.customer).first()
                if cart:
                    cart.items.clear()
                
                return JsonResponse({
                    'status': 'success',
                    'order_id': order.order_id,
                    'message': 'Payment successful'
                })
            except razorpay.errors.SignatureVerificationError:
                order = Order.objects.get(razorpay_order_id=razorpay_order_id)
                order.status = 'FAILED'
                order.save()
                return JsonResponse({'status': 'error', 'message': 'Payment verification failed'}, status=400)
                
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_success_page(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        return render(request, 'payment_success.html', {'order': order})
    except Order.DoesNotExist:
        return render(request, 'payment_failure.html', {'message': 'Order not found'})

def payment_failure_page(request):
    return render(request, 'payment_failure.html', {'message': 'Payment failed. Please try again.'})
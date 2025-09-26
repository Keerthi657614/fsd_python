# # website/views.py

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login as auth_login
# from django.http import JsonResponse, HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import Product, Review
# from .forms import CustomUserCreationForm # Assuming you have a forms.py with this form
# from decimal import Decimal #
# from .forms import ReviewForm # Import the form

# # --- AUTHENTICATION VIEWS ---
# from django.contrib.auth import logout as auth_logout
# def signup(request):
#     """Handles user registration."""
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             return redirect('product_list')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'website/signup.html', {'form': form})

# @csrf_exempt
# def login(request):
#     """Handles custom login logic (POST) and displays the form (GET)."""
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             auth_login(request, user)
#             return redirect('product_list')
#         else:
#             context = {'error_message': 'Invalid username or password.'}
#             return render(request, "website/login.html", context) 
            
#     return render(request, "website/login.html") 

# def logout(request):
#     """Placeholder for logout page display (actual logout handled in base.html form)."""
#     return render(request, "website/logout.html")

# # --- CORE E-COMMERCE VIEWS ---

# # Renamed 'home' to be consistent with 'product_list' function.
# # The URL router determines which function runs for the '/' path.
# @login_required 
# def product_list(request):
#     """Displays the main product catalog (requires login)."""
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'website/product_list.html', context)

# # def product_detail(request, pk):
# #     """Displays details for a single product."""
# #     product = get_object_or_404(Product, pk=pk)
# #     # Assuming the existence of the Review model for context
# #     reviews = product.reviews.all()
# #     context = {'product': product, 'reviews': reviews}
# #     return render(request, 'website/product_detail.html', context)
# def product_detail(request, pk):
#     """Displays details for a single product with reviews and form."""
#     product = get_object_or_404(Product, pk=pk)
#     reviews = product.reviews.all()
#     form = ReviewForm()  # Empty form for GET

#     context = {
#         'product': product,
#         'reviews': reviews,
#         'form': form,
#     }
#     return render(request, 'website/product_detail.html', context)


# # --- CART MANAGEMENT VIEWS ---

# @login_required
# def add_to_cart(request, pk):
#     """Adds a product (by ID) to the user's session cart."""
#     if request.method == 'POST':
#         cart = request.session.get('cart', [])
#         pk_int = int(pk)
        
#         if pk_int not in cart:
#              cart.append(pk_int)

#         request.session['cart'] = cart
#         request.session.modified = True
        
#     return redirect('cart')

# @login_required
# def remove_from_cart(request, pk):
#     """Removes a product (by ID) from the user's session cart."""
#     if request.method == 'POST':
#         cart = request.session.get('cart', [])
#         pk_int = int(pk)
        
#         # Removes the item by filtering out all matching IDs
#         new_cart = [item_id for item_id in cart if item_id != pk_int]

#         request.session['cart'] = new_cart
#         request.session.modified = True
        
#     return redirect('cart')

# @login_required
# def cart(request):
#     cart_ids = request.session.get('cart', [])
#     cart_products = Product.objects.filter(id__in=cart_ids)
    
#     # --- CALCULATE TOTALS ---
#     subtotal = sum(product.price for product in cart_products)
    
#     # FIX: Define shipping as a Decimal to match the subtotal type
#     shipping = Decimal('0.00') # <--- CONVERT TO DECIMAL TYPE
    
#     # Line 107: This calculation now works because both operands are Decimal
#     order_total = subtotal + shipping 
    
#     context = {
#         'cart_products': cart_products,
#         'subtotal': subtotal,
#         'shipping': shipping,
#         'order_total': order_total,
#     }
#     return render(request, 'website/cart.html', context)

# @login_required
# def checkout(request):
#     """Handles the final checkout process and clears the cart."""
#     if request.method == 'POST':
#         print("Order processed successfully!")
        
#         if 'cart' in request.session:
#             del request.session['cart']
            
#         return redirect('order_confirmation')
    
#     return redirect('cart')

# def order_confirmation(request):
#     """Displays the order confirmation page after checkout."""
#     return render(request, 'website/order_confirmation.html')

# # --- API/ADMIN VIEWS (Kept separate as requested) ---

# def search(request):
#     """Placeholder for a search functionality."""
#     return render(request, "website/index.html", {
#         'products': [],
#         'title': 'Search Products',
#         'description': 'Search for products here.'
#     })

# @csrf_exempt
# def product_add(request):
#     """API endpoint to add a product."""
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             product = Product.objects.create(
#                 name=data.get("name"), description=data.get("description"),
#                 price=data.get("price"), stock=data.get("stock")
#             )
#             return JsonResponse({"id": product.id, "name": product.name, "description": product.description, "price": str(product.price), "stock": product.stock})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     return HttpResponseBadRequest("Invalid request method")

# @csrf_exempt
# def product_update(request, id):
#     """API endpoint to update a product."""
#     if request.method == "PUT":
#         try:
#             data = json.loads(request.body)
#             product = Product.objects.get(pk=id)
#             product.name = data.get("name", product.name)
#             product.description = data.get("description", product.description)
#             product.price = data.get("price", product.price)
#             product.stock = data.get("stock", product.stock)
#             product.save()
#             return JsonResponse({"id": product.id, "name": product.name, "description": product.description, "price": str(product.price), "stock": product.stock})
#         except Product.DoesNotExist:
#             return JsonResponse({"error": "Product not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     return HttpResponseBadRequest("Invalid request method")
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# @login_required
# def add_review(request, pk):
#     """Handles submission of a review form for a specific product."""
#     product = get_object_or_404(Product, pk=pk)

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.product = product
#             review.user = request.user   # ✅ Attach logged-in user
#             review.save()
#             messages.success(request, "Your review has been added successfully.")
#             return redirect('product_detail', pk=product.pk)
#         else:
#             # Show validation errors
#             messages.error(request, "There was an error with your review. Please try again.")
#             return render(request, 'website/product_detail.html', {
#                 'product': product,
#                 'reviews': product.reviews.all(),
#                 'form': form
#             })

#     # Fallback
#     return redirect('product_detail', pk=product.pk)

#     """Handles submission of a review form for a specific product."""
#     product = get_object_or_404(Product, pk=pk)
    
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.product = product
#             # In a real app, you would also set review.user = request.user
#             review.save()
#             # Redirect back to the product detail page after successful submission
#             return redirect('product_detail', pk=product.pk)
    
#     # If not a POST or form is invalid, simply redirect back
#     return redirect('product_detail', pk=product.pk) 



# website/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json

from .models import Product, Review
from .forms import CustomUserCreationForm, ReviewForm

# =========================
# AUTHENTICATION VIEWS
# =========================
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'website/signup.html', {'form': form})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('product_list')
        else:
            context = {'error_message': 'Invalid username or password.'}
            return render(request, "website/login.html", context) 
    return render(request, "website/login.html")

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')
def search(request):
    """Placeholder for a search functionality."""
    return render(request, "website/index.html", {
        'products': [],
        'title': 'Search Products',
        'description': 'Search for products here.'
    })

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'website/product_list.html', {'products': products})

from django.shortcuts import redirect

def home_redirect(request):
    """Redirect root URL to login or product list."""
    if request.user.is_authenticated:
        return redirect('product_list')
    else:
        return redirect('login')

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')
    form = ReviewForm()
    context = {
        'product': product,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'website/product_detail.html', context)


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user   # associate review with logged-in user
            review.save()
            return redirect('product_detail', pk=product.pk)
    return redirect('product_detail', pk=product.pk)


# =========================
# CART VIEWS
# =========================
@login_required
def add_to_cart(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        pk_int = int(pk)
        if pk_int not in cart:
            cart.append(pk_int)
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')


@login_required
def remove_from_cart(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        pk_int = int(pk)
        cart = [item for item in cart if item != pk_int]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')


@login_required
def cart(request):
    cart_ids = request.session.get('cart', [])
    cart_products = Product.objects.filter(id__in=cart_ids)
    subtotal = sum(product.price for product in cart_products)
    shipping = Decimal('0.00')
    order_total = subtotal + shipping
    context = {
        'cart_products': cart_products,
        'subtotal': subtotal,
        'shipping': shipping,
        'order_total': order_total,
    }
    return render(request, 'website/cart.html', context)


@login_required
def checkout(request):
    if request.method == 'POST':
        if 'cart' in request.session:
            del request.session['cart']
        return redirect('order_confirmation')
    return redirect('cart')


def order_confirmation(request):
    return render(request, 'website/order_confirmation.html')


# =========================
# PRODUCT API VIEWS
# =========================
@csrf_exempt
def product_add(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product = Product.objects.create(
                name=data.get("name"), 
                description=data.get("description"),
                price=data.get("price"), 
                stock=data.get("stock")
            )
            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return HttpResponseBadRequest("Invalid request method")

def product_list(request):
    """Displays all products."""
    products = Product.objects.all()
    return render(request, 'website/product_list.html', {'products': products})
@csrf_exempt
def product_update(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            product = Product.objects.get(pk=id)
            product.name = data.get("name", product.name)
            product.description = data.get("description", product.description)
            product.price = data.get("price", product.price)
            product.stock = data.get("stock", product.stock)
            product.save()
            return JsonResponse({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock": product.stock
            })
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return HttpResponseBadRequest("Invalid request method")

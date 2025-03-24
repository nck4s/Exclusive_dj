from django.shortcuts import render, redirect
from .models import Product, Category, CartItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomSignupForm
from django.http import JsonResponse
from .models import Product, WishlistItem

from django.views.decorators.http import require_POST


def home(request):
    products = Product.objects.filter(available=True)
    best_selling_products = products.order_by('-id')[:4]
    categories = Category.objects.all()

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'home.html', {
        'products': products,
        'best_selling_products': best_selling_products,
        'categories': categories,
        'wishlist_product_ids': list(wishlist_product_ids),
    })



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'product_detail.html', {'product': product})


# Добавить в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# Удалить из корзины
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

# Обновить количество
@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        new_qty = int(request.POST.get('quantity', 1))
        item.quantity = new_qty
        item.save()
    return redirect('cart')

# Просмотр корзины
@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })




def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})


from .forms import CustomLoginForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


from .models import WishlistItem


@login_required
def wishlist_view(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_from_wishlist(request, product_id):
    WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@require_POST
@login_required
def toggle_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

    if created:
        return JsonResponse({'status': 'added'})
    else:
        item.delete()
        return JsonResponse({'status': 'removed'})
from django.shortcuts import render, redirect
from .models import Product, Category, CartItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()

    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, available=True)
    else:
        products = Product.objects.filter(available=True)

    best_selling_products = Product.objects.filter(available=True).order_by('-sold_count')[:4]

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'best_selling_products': best_selling_products,
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
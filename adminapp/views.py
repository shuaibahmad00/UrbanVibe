from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from main.models import Product, Order
from userapp.models import * # Assuming user app doesn't have specific models yet but importing for completeness if needed
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

# Check if user is superuser
def is_admin(user):
    return user.is_superuser

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You are not authorized to access this area.')
    else:
        form = AuthenticationForm()
    return render(request, 'adminapp/login.html', {'form': form})

@user_passes_test(is_admin, login_url='/admin_features/login/')
def admin_dashboard(request):
    return render(request, 'adminapp/dashboard.html')

@user_passes_test(is_admin, login_url='/admin_features/login/')
def view_users(request):
    users = User.objects.all()
    return render(request, 'adminapp/view_users.html', {'users': users})

@user_passes_test(is_admin, login_url='/admin_features/login/')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        
        Product.objects.create(
            name=name, price=price, description=description, 
            category=category, image=image
        )
        return redirect('view_products')
    return render(request, 'adminapp/add_product.html')

@user_passes_test(is_admin, login_url='/admin_features/login/')
def view_products(request):
    products = Product.objects.all()
    return render(request, 'adminapp/view_products.html', {'products': products})

@user_passes_test(is_admin, login_url='/admin_features/login/')
def view_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'adminapp/view_orders.html', {'orders': orders})

@user_passes_test(is_admin, login_url='/admin_features/login/')
def sales_report(request):
    orders = Order.objects.filter(status='Delivered') # Assuming 'Delivered' means sold
    total_sales = sum(order.product.price * order.quantity for order in orders)
    count = orders.count()
    return render(request, 'adminapp/sales_report.html', {'total_sales': total_sales, 'count': count})

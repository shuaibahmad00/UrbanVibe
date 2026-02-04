from django.shortcuts import render, redirect
from .models import Product, Contact, Collection

# Create your views here.
def home(request):
    collections_list = Collection.objects.all()
    return render(request, 'home.html', {'collections': collections_list})

def collections(request):
    products = Product.objects.all()
    return render(request, 'collections.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        return redirect('home')
    return render(request, 'contact.html')
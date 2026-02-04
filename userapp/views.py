from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import send_registration_email
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')

        # Simple validation: username will be the email/email-part for this simple example 
        # or we can use email as username if needed. Let's use email as username.
        if User.objects.filter(username=email).exists():
            messages.error(request, 'User with this email already exists.')
            return render(request, 'userapp/register.html')

        try:
            # Create User
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = full_name
            user.save()

            # Create Profile
            UserProfile.objects.create(
                user=user,
                address=address,
                contact_no=phone,
                pincode=pincode
            )

            # Send Email
            send_registration_email(email, full_name)

            # Login user
            login(request, user)
            messages.success(request, 'Registration successful! Welcome email sent.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'userapp/register.html')
            
    return render(request, 'userapp/register.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'userapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

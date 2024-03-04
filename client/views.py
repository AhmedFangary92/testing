from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Client

    
def client_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    elif request.method == 'POST':
        # Get the form data from the POST request
        first_name = request.POST['first_name'].capitalize()
        last_name = request.POST['last_name'].capitalize()
        username = request.POST['username'].lower()
        email = request.POST['email'].lower()
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # Validate the form data
        if not username or not email or not password1 or not password2:
            error = 'من فضلك املئ جميع الحقول'
        elif password1 != password2:
            error = 'كلمات المرور لا تتطابق'
        elif User.objects.filter(email=email).exists():
            error = 'هذا البريد الاكتروني مسجل من قبل'
        elif Client.objects.filter(phone=phone).exists():
            error = 'هذا الرقم مسجل من قبل'
        elif User.objects.filter(username=username).exists():
            error = 'اسم المستخدم مسجل من قبل'
        else:
            # Create a new user account
            user = User.objects.create_user(first_name=first_name, 
                                            last_name=last_name,
                                            username=username, 
                                            email=email,
                                            password=password1)
            # Create a new client object associated with the user
            client = Client.objects.create(user=user,
                                           phone=phone)
            # Add success message and redirect to login page
            messages.success(request, 'التسجيل اكتمل، يمكنك تسجيل الدخول.')
            # Redirect to the login page
            return redirect('login')
        # If there was an error, render the registration form with the error message
        return render(request, 'client/register.html', {'error': error})
    else:
        return render(request, 'client/register.html')


def client_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    elif request.method == 'POST':
        # Get the form data from the POST request
        identification = request.POST['text'].lower()
        password = request.POST['password']
        # Check if the identification is a username or a phone number
        user = None
        if User.objects.filter(username=identification).exists():
            user = User.objects.get(username=identification)
        elif Client.objects.filter(phone=identification).exists():
            client = Client.objects.get(phone=identification)
            user = client.user

        # Authenticate the user
        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                # Log the user in and redirect to the home page
                login(request, user)
                return redirect('home')

        # If authentication fails, render the login page with an error message
        error = 'خطأ في اسم المستخدم او كلمة المرور'
        return render(request, 'client/login.html', {'error': error})

    else:
        return render(request, 'client/login.html')


def client_logout(request):
    logout(request)
    return redirect('home')


def client_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'client/profile.html')


def client_profile_update(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    user = request.user
    client = user.client
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            if new_password:
                user.set_password(new_password)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            client.phone = phone

        user.save()
        client.save()

        return redirect('profile')

    else:
        error_message = "كلمة المرور الجديدة غير متطابقة."
        return render(request, 'client/profile.html', {'error_message': error_message})
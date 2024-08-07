
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User  # Ensure this is your custom User model
from django.contrib.auth.hashers import make_password, check_password

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username already exists.'}, status=400)
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already registered.'}, status=400)
            
            hashed_password = make_password(password)
            try:
                new_user = User.objects.create(username=username, email=email, password=hashed_password)
                new_user.save()
                return JsonResponse({'message': 'Successfully registered!'})
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            return JsonResponse({'message': 'Passwords do not match.'}, status=400)
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            return JsonResponse({'message': 'Login successful!'})
        else:
            return JsonResponse({'message': 'Invalid credentials.'}, status=400)
    
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from .forms import RegisterForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .cutom_backend import CustomAuthBackend
from .models import CustomUser
from django.contrib import messages

#eveluating reg req
# @csrf_exempt
# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         # print(form)
#         print(form.is_valid())
#         if form.is_valid():
#             print(form.is_valid())
#             # Log the user in after registration
#             username = request.POST['username']
#             email = request.POST['email']
#             password = request.POST['password2']
#             print(username , password ,password )
#             if CustomUser.objects.filter(email = email).exists():
#                 messages.error(request, "Invalid email or password")
#                 return render(request, 'register/register.html', {'form': form})
#             print(email)
#             user_extra = authenticate(username=username, password=password)
#             form.save()
#             user = CustomUser.objects.get(email=email)
#             print(user_extra)
#             # Retrieve the user object
#             #user = form.cleaned_data.get('username')
#             login(request, user,backend='django.contrib.auth.backends.ModelBackend')
#             context = {
#                 'username': user.username,
#             }
#             print(user.username)
#             return render(request, 'transactions/make_payment.html', context)  # Redirect to home page after registration
#             # return redirect('/make_payment/',username=request.user.username)
#     else:
#         form = RegisterForm()
#     return render(request, 'register/register.html', {'form': form})

# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from .models import CustomUser
# from django.shortcuts import render, redirect

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Get data from request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        
        if password != confirm_password:
            messages.error(request, "password confirm password didn't match")
            return render(request, 'register/register.html')


        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "A user with that username already exists.")
            return render(request, 'register/register.html')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with that Email already exists.")
            return render(request, 'register/register.html')
        
        # Create user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        
        # Log in the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context = {
                'username': user.username,
            }
            return render(request, 'transactions/make_payment.html', context)
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'register/register.html')

    else:
        return render(request, 'register/register.html')



# evaluating login req
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        # print('helloo')
        form = EmailAuthenticationForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            user = CustomAuthBackend().authenticate(request = request, email=email, password=password)
            if user is not None:# Retrieve the user object
                print(type(user))
                login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password")

        return render(request, 'register/login.html', {'form': form})
    else:
        form = EmailAuthenticationForm()
        return render(request, 'register/login.html', {'form': form})

#evaluating logout req!
@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

#home view
@csrf_exempt
def home(request):
    user = request.user
    # Add any context data you want to pass to the template
    context = {
        'current_user': user,
    }
    return render(request, 'core/home.html', context=context)
    return redirect('/home',current_user=user)


def view_transactions(request):
    return render(request, 'core/view_transaction.html')
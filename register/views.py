from django.shortcuts import render, redirect
from .forms import EmailAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from .cutom_backend import CustomAuthBackend
from .models import CustomUser
from django.contrib import messages


# from django.http import HttpResponse


# Register handler
@csrf_protect
def register(request):
    """
    :param request: Http request
    :return: blank form (GET), redirects to home page (POST
    """
    if request.method == 'POST':

        # Get data from request
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        currency = request.POST.get('currency')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')


        # Checking Password
        if password != confirm_password:
            messages.error(request, "password confirm password didn't match")
            return render(request, 'register/register.html')

        # Verifying username
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "A user with that username already exists.")
            return render(request, 'register/register.html')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with that Email already exists.")
            return render(request, 'register/register.html')

        # Create user in database

        user = CustomUser.objects.create_user(
            username=username, firstName=firstName, lastName=lastName,
            email=email, currency=currency, password=password)

        # Log in the user via authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context = {
                'username': user.username,
            }
            return render(request, 'transactions/make_payment.html', context)
        # Handling invalid user
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'register/register.html')

    # Initial view(GET req)
    else:
        return render(request, 'register/register.html')


# evaluating login req
@csrf_protect
def user_login(request):
    """
    :param request: http request
    :return: login form (GET), redirect to home (POST)
    """
    if request.method == 'POST':
        # print('helloo')

        # Custom auth call
        form = EmailAuthenticationForm(data=request.POST)

        # Form Validation
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # User verification using custom backend
            user = CustomAuthBackend().authenticate(request=request, email=email, password=password)
            if user is not None:  # Retrieve the user object
                print(type(user))
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password")  # invalid user response

        return render(request, 'register/login.html', {'form': form})
    else:
        form = EmailAuthenticationForm()
        return render(request, 'register/login.html', {'form': form})


# Evaluating logout req!
@csrf_protect
def user_logout(request):
    logout(request)
    return redirect('/')  # Redirect to home page after logout


# Home view
@csrf_protect
def home(request):
    """
    :param request: http request
    :return: html with context
    """
    user = request.user
    # Add any context data you want to pass to the template
    context = {
        'current_user': user,
    }
    return render(request, 'core/home.html', context=context)
    # return redirect('/home',current_user=user)


# View transaction logic
@csrf_protect
def view_transactions(request):
    """
    :param request: http request
    :return: view transaction template
    """
    return render(request, 'core/view_transaction.html')

from django.shortcuts import render, redirect
from .forms import RegisterForm, EmailAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

#eveluating reg req
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in after registration
            email = request.POST['email']
            password = request.POST['password2']
            user = authenticate(username=email, password=password)  # Retrieve the user object
            #user = form.cleaned_data.get('username')
            login(request, user)
            return redirect('home')  # Redirect to home page after registration
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})


#evaluating login req
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        print(form.is_valid())
        print(form.cleaned_data)
        print(form.errors)
        if form:
            email = request.POST['email']
            password = request.POST['password']
            print(email, password)
            user = authenticate(email=email, password=password)  # Retrieve the user object
            print(type(user))
            login(request, user)
            return redirect('home')
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
def home(request):
    user = request.user
    # Add any context data you want to pass to the template
    context = {
        'current_user': user,
    }
    return render(request, 'core/home.html', context=context)


def view_transactions(request):
    return render(request, 'core/view_transaction.html')
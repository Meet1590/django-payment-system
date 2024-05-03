"""
URL configuration for webapps2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from currencyConverterApp import views as currencyConverterApp
from register import views as registerApp
from payapp import views as payApp

urlpatterns = (
    path('admin/', admin.site.urls),
    path('register/', registerApp.register, name='register'),
    path('login/', registerApp.user_login, name='login'),
    path("", registerApp.home, name='home'),
    path('make_payment/', payApp.make_payment, name='make_payment'),
    path('view_transactions/', registerApp.view_transactions, name='view_transactions'),
    path('convert_currency/<str:currency1>/<str:currency2>/<int:amount>/', currencyConverterApp.convert_currency,
         name='convert_currency'),
    path('view_user_transactions/', payApp.view_user_transactions, name='view_user_transactions'),
    path('create-payment-request/', payApp.create_payment_request, name='create_payment_request'),
    path('pending-requests/', payApp.list_pending_requests, name='pending_requests'),
    path('handle-response/<int:request_id>/', payApp.handle_response_to_request, name='handle_response_to_request'),
    path('logout/', registerApp.user_logout, name='logout')
)

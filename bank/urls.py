"""restbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import UserRegisterView,UserLoginview,CreateAccountView,Balance,Withdrawview,Depositview,Transactionview

urlpatterns = [
    path('register',UserRegisterView.as_view()),
    path('login',UserLoginview.as_view()),
    path("createac",CreateAccountView.as_view()),
    path("balance/<int:acc_no>",Balance.as_view()),
    path("withdraw/<int:acc_no>",Withdrawview.as_view()),
    path("deposit/<int:acc_no>",Depositview.as_view()),
    path("transaction",Transactionview.as_view()),
    path("view_transaction/<int:acc_no",Transactionview.as_view())




]

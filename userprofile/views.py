from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import http
# Create your views here.
from products.models import Category
from rest_framework.authtoken.models import Token
from userprofile.forms import ContactForm, SignUpForm, LoginForm
from userprofile.models import Seller, Contact, Buyer
from django.contrib import messages



def sellers_view(request):
    categories = Category.objects.all()
    sellers = Seller.objects.all()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
        'categories': categories,
        'sellers': sellers,
    }
    return render(request, 'userprofile/sellers.html', context)


def vendor_view(request, pk):
    categories = Category.objects.all()
    seller = Seller.objects.get(id=pk)
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    rate = seller.rate / seller.number_of_rates
    if rate % 1 == 0:
        flag = 2
    else:
        flag = 1

    context = {
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
        'categories': categories,
        'seller': seller,
        "rate": (rate//1),
        "remainder": rate % 1,
        "the_rate": rate,
        "range": range(1, int(rate//1+1)),
        "range2": range(1, int(5-(rate//1+1))+flag)
    }
    return render(request, 'userprofile/vendor.html', context)


def we_view(request):
    categories = Category.objects.all()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'categories': categories,
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
    }
    return render(request, 'userprofile/we.html', context)


def contact_view(request):
    categories = Category.objects.all()
    form = ContactForm()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
        'categories': categories,
        'form': form
    }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            contact = Contact()
            contact.name = name
            contact.phone = phone
            contact.email = email
            contact.message = message
            contact.save()
            return render(request, 'userprofile/contact.html', context)

    return render(request, 'userprofile/contact.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            re_password = cd['re_password']
            if len(User.objects.filter(username=username)) > 0:
                messages.add_message(request, messages.ERROR, 'this username is already exists')
                return HttpResponseRedirect('/')

            if password != re_password:
                messages.add_message(request, messages.ERROR, 'the password fields doesn\'t match')
                return HttpResponseRedirect('/')
            user = User.objects.create_user(username, cd['email'], password)
            user.save()
            buyer = Buyer(user=user)
            buyer.save()
            Token.objects.create(user=user)
            messages.add_message(request, messages.SUCCESS, 'user has been added')
            return HttpResponseRedirect('/')


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            userbyemail = User.objects.filter(email=username)
            if len(userbyemail) > 0:
                user = authenticate(username=userbyemail[0].username, password=password)
            if user is not None and not user.is_superuser:
                login(request, user)

                if not form.cleaned_data['remember_me']:
                    request.session.set_expiry(0)
            else:
                messages.add_message(request, messages.ERROR, 'bad credentials')
            return HttpResponseRedirect('/')


def log_out(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'ha cerrado la sesión con éxito')
    return HttpResponseRedirect('/')
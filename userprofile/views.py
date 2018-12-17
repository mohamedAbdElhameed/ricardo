from decimal import Decimal

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import http
# Create your views here.
from products.models import Category
from rest_framework.authtoken.models import Token
from userprofile.forms import ContactForm, SignUpForm, LoginForm, PasswordForm
from userprofile.models import Seller, Contact, Buyer
from django.contrib import messages


def sellers_view(request):
    categories = Category.objects.all()
    sellers = Seller.objects.all()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    positions = []
    for seller in sellers:
        positions.append([seller.city.name, float(seller.latitude), float(seller.longitude)])
    context = {
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
        'categories': categories,
        'sellers': sellers,
        'positions': positions,
    }
    return render(request, 'userprofile/sellers.html', context)


def vendor_view(request, pk):
    categories = Category.objects.all()
    seller = Seller.objects.get(id=pk)
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    if seller.number_of_rates == 0:
        rate = 0
    else:
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
            email = cd['email']
            if len(User.objects.filter(username=username)) > 0:
                messages.add_message(request, messages.ERROR, 'this username is already exists')
                return HttpResponseRedirect('/')

            if len(User.objects.filter(email=email)) > 0:
                messages.add_message(request, messages.ERROR, 'this email is already exists')
                return HttpResponseRedirect('/')

            if password != re_password:
                messages.add_message(request, messages.ERROR, 'the password fields doesn\'t match')
                return HttpResponseRedirect('/')
            user = User.objects.create_user(username, email, password)
            user.save()
            buyer = Buyer(user=user)
            buyer.save()
            Token.objects.create(user=user)
            messages.add_message(request, messages.SUCCESS, 'user has been added')
            return HttpResponseRedirect('/')


def authenticate_via_email(email, password):
    """
        Authenticate user using email.
        Returns user object if authenticated else None
    """
    if email:
        try:
            user = User.objects.get(email__iexact=email)
            print(user)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            pass
    return None


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


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Password changed successfully.')
            update_session_auth_hash(request, form.user)
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'settings/password.html', {'form': form})


@login_required(login_url='/')
def profile(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,

    }

    return render(request, 'userprofile/profile.html', context)
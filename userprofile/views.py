import os
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from PIL import Image
from django import http
# Create your views here.
from products.models import Category
from rest_framework.authtoken.models import Token
import time
from ricardo import settings
from userprofile.forms import ContactForm, SignUpForm, LoginForm, PasswordForm, ProfileForm
from userprofile.models import Seller, Contact, Buyer
from django.contrib import messages


def sellers_view(request):
    categories = Category.objects.all()
    sellers = Seller.objects.all()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    positions = []
    for seller in sellers:
        if seller.city:
            positions.append([seller.city.name, float(seller.latitude), float(seller.longitude)])
        else:
            positions.append(['city', float(seller.latitude), float(seller.longitude)])

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
    print(seller.reviews)
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
        "rate": (rate // 1),
        "remainder": rate % 1,
        "the_rate": rate,
        "range": range(1, int(rate // 1 + 1)),
        "range2": range(1, int(5 - (rate // 1 + 1)) + flag)
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
            messages.add_message(request, messages.SUCCESS,
                                 'El usuario ha sido registrado, por favor ingrese con sus datos.')
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
                messages.add_message(request, messages.ERROR, 'Datos incorrectos')
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


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Contraseña cambiada con éxito.')
            update_session_auth_hash(request, form.user)
        else:
            messages.error(request, u'Por favor, corrija el error a continuación.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'userprofile/change_password.html', {'form': form})


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET['upload_picture'] == 'uploaded':
            uploaded_picture = True
    except Exception:
        uploaded_picture = False
    return render(request, 'userprofile/picture.html', {'uploaded_picture': uploaded_picture})


@login_required
def upload_picture(request):
    try:
        f = request.FILES['picture']
        ext = os.path.splitext(f.name)[1].lower()
        valid_extensions = ['.gif', '.png', '.jpg', '.jpeg', '.bmp']
        if ext in valid_extensions:
            filename = settings.MEDIA_ROOT + '/' + request.user.username + '_tmp.jpg'
            with open(filename, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            im = Image.open(filename)
            width, height = im.size
            if width > 560:
                new_width = 560
                new_height = (height * 560) / width
                new_size = new_width, new_height
                im.thumbnail(new_size, Image.ANTIALIAS)
                im.save(filename)
            return redirect('/userprofile/picture/?upload_picture=uploaded')
        else:
            messages.error(request, u'Invalid file format.')
    except Exception:
        print(Exception)
        messages.error(request, u'An expected error occurred.')
    return redirect('/userprofile/picture/')


@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST['x'])
        y = int(request.POST['y'])
        w = int(request.POST['w'])
        h = int(request.POST['h'])
        time_now = str(int(round(time.time() * 1000)))
        tmp_filename = settings.MEDIA_ROOT + '/' + request.user.username + '_tmp.jpg'
        filename = settings.MEDIA_ROOT + '/' + request.user.username + time_now + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w + x, h + y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)
        buyer = request.user.buyer
        buyer.avatar = request.user.username + time_now + '.jpg'
        buyer.save()
        return HttpResponse(settings.MEDIA_URL + '/' + request.user.username + time_now + '.jpg')
    except Exception:
        return HttpResponseBadRequest()


@login_required
def profile_change(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.buyer)
        if form.is_valid():
            form.save()
            messages.success(request, u'Su perfil se ha actualizado correctamente.')
            return redirect('userprofile:profile_change')
    else:
        form = ProfileForm(instance=request.user.buyer)
    return render(request, 'userprofile/profile_edit.html', {'form': form})

from django.shortcuts import render
from django import http
# Create your views here.
from products.models import Category
from userprofile.forms import ContactForm
from userprofile.models import Seller, Contact


def sellers_view(request):
    categories = Category.objects.all()
    sellers = Seller.objects.all()
    context = {
        'categories': categories,
        'sellers': sellers,
    }
    return render(request, 'userprofile/sellers.html', context)


def vendor_view(request, pk):
    categories = Category.objects.all()
    seller = Seller.objects.get(id=pk)
    rate = seller.rate / seller.number_of_rates
    if rate % 1 == 0:
        flag = 2
    else:
        flag = 1

    context = {
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

    context = {
        'categories': categories,

    }
    return render(request, 'userprofile/we.html', context)


def contact_view(request):
    categories = Category.objects.all()
    form = ContactForm()
    context = {
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
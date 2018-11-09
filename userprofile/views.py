from django.shortcuts import render

# Create your views here.
from products.models import Category
from userprofile.models import Seller


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
from django.shortcuts import render

# Create your views here.
from products.models import Category
from stories.models import ArtisanMaster, Tale
from userprofile.forms import SignUpForm, LoginForm


def masters_view(request):
    masters = ArtisanMaster.objects.all()
    categories = Category.objects.all()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'categories': categories,
        'masters': masters,
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
    }

    return render(request, 'stories/artisan_master.html', context)


def tales_view(request):
    tales = Tale.objects.all()
    categories = Category.objects.all()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'categories': categories,
        'tales': tales,
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
    }

    return render(request, 'stories/tales.html', context)

from django.shortcuts import render
# Create your views here.
from products.models import Category

from start.models import StartDetail
from userprofile.forms import SignUpForm, LoginForm


def index(request):
    categories = Category.objects.all()
    start = StartDetail.objects.last()
    sign_up_form = SignUpForm()
    sign_in_form = LoginForm()
    context = {
        'categories': categories,
        'start': start,
        'sign_up_form': sign_up_form,
        'sign_in_form': sign_in_form,
    }
    return render(request, 'start/index.html', context)

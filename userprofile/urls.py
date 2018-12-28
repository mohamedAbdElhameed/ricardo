from django.conf.urls import url
from django.urls import path, include

from products.views import sub_categories, products_view, product_view
from userprofile.views import *
from userprofile.apis.views import *

from . import views

app_name = 'userprofile'

urlpatterns = [
    path('api/seller/<int:pk>/', SellerDetailView.as_view(), name='seller_endpoint_detail'),
    path('api/contact/', ContactView.as_view(), name='contact_endpoint'),
    path('api/sellers/', SellersView.as_view(), name='sellers'),
    path("api/register/", UserCreate.as_view(), name="user_create"),
    path("api/login/", LoginView.as_view(), name="login"),
    path('api/review/', ReviewView.as_view()),
    path('sellers/', sellers_view, name='sellers'),
    path('vendor/<int:pk>/', vendor_view, name='vendor'),
    path('we/', we_view, name='we'),
    path('contact/', contact_view, name='contact'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', log_out, name='logout'),
    path('profile/', profile, name='profile'),
    path('password/', password, name='change_password'),
    path('picture/', picture, name='picture'),
    url(r'^upload_picture/$', upload_picture, name='upload_picture'),
    url(r'^save_uploaded_picture/$', save_uploaded_picture, name='save_uploaded_picture'),
]
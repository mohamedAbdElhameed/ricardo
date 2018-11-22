from django.urls import path, include

from products.views import sub_categories, products_view, product_view
from userprofile.views import sellers_view, vendor_view, we_view, contact_view, signup, signin, log_out
from userprofile.apis.views import SellerDetailView, ContactView, SellersView, UserCreate, LoginView

from . import views

app_name = 'userprofile'

urlpatterns = [
    path('api/seller/<int:pk>/', SellerDetailView.as_view(), name='seller_endpoint_detail'),
    path('api/contact/', ContactView.as_view(), name='contact_endpoint'),
    path('api/sellers/', SellersView.as_view(), name='sellers'),
    path("api/register/", UserCreate.as_view(), name="user_create"),
    path("api/login/", LoginView.as_view(), name="login"),
    path('sellers/', sellers_view, name='sellers'),
    path('vendor/<int:pk>/', vendor_view, name='vendor'),
    path('we/', we_view, name='we'),
    path('contact/', contact_view, name='contact'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', log_out, name='logout')
]
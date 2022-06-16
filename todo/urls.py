from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('lists_products/', list_products, name='lists_products'),
    path('lists_products/<slug:products_slug>/', products, name='products'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('personal_account/', personal_account, name='personal_account'),
    path('todo/', todo, name='todo'),
   # path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]

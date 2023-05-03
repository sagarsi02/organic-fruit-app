from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('createUser/', views.createUser, name='createUser'),
   path('userLogin/', views.userLogin, name='userLogin'),
   path('userLogout/', views.userLogout, name='userLogout'),
   path('cart/<int:user_id>/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
   path('basket_list/', views.basket_list, name='basket_list'),
   path('basket/', views.basket, name='basket')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
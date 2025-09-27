from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('add_to_cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('order_placed/', views.payment_done, name='order_placed'),
    path('staff_order/', views.staff_order, name='staff_order'),
    path('all_order/', views.All_Order, name='all_order'),
    path('staff/', views.Staff, name='staff'),
    path('staff/view/<int:pk>/', views.staff_detail , name='dashboard-staff-detail'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    path('register/', views.SignUp, name='signup'),
    path('', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.Profile, name='user-profile'),
    path('profile/update/', views.Profile_update, name='user-profile-update'),

]+ static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
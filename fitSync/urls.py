from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),    
    path('services/', views.services, name='services'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('zumba/', views.zumba, name='zumba'),
    path('hiit/', views.hiit, name='hiit'),
    path('yoga/', views.yoga, name='yoga'),
    path('bookings/', views.get_bookings, name='bookings'),
    path('book-class/', views.book_class, name='book_class'),
    path('classes/', views.get_classes, name='get_classes'),

]

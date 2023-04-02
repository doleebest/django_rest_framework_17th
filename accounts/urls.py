from django.urls import path
from django.contrib.auth import views as auth_views
#from accounts.views import home
from .views import register
urlpatterns = [
#    path('', home),
    path('login', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path('logout',auth_views.LoginView.as_view(template_name='accounts/logout.html')),
    path('register/', register, name='register')
]
#from .views import register, login, logout
#urlpatterns = [
#    path('register/', register, name='register'),
#    path('login/', login, name='login'),
#    path('logout/', logout, name='logout'),
#]
from django.urls import path
from . import views


urlpatterns = [
	path('', views.index_view, name='index'),
    path('login/', views.membro_login_view, name='login'),
	path('hello/', views.hello_world, name='hello-world')
]

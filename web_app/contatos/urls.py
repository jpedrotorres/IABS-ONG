from django.urls import path
from . import views


urlpatterns = [
	path("", views.index_view, name="index"),
	path("parceiros/", views.parceiro_view, name="parceiro_page"),
	path("reunioes/", views.reuniao_view, name="reuniao_page"),
    path("login/", views.membro_login_view, name="login"),
	path("logout/confirm/", views.logout_confirm_modal_view, name="logout_confirm"),
	path("logout/", views.membro_logout_view, name="logout"),
	path("hello/", views.hello_world, name="hello-world")
]

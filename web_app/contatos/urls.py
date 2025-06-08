from django.urls import path
from . import views


urlpatterns = [
	path("", views.index_view, name="index"),
	path("parceiros/", views.parceiro_view, name="parceiro_page"),
	path("reunioes/", views.reuniao_view, name="reuniao_page"),
	path('parceiros/<int:pk>/', views.generic_detail_view, {'entity_type': 'parceiro'}, name='parceiro_detail'),
	path('reunioes/<int:pk>/', views.generic_detail_view, {'entity_type': 'reuniao'}, name='reuniao_detail'),
	path('parceiros/<int:pk>/editar/', views.generic_edit_view, {'entity_type': 'parceiro'}, name='parceiro_edit'),
	path('reunioes/<int:pk>/editar/', views.generic_edit_view, {'entity_type': 'reuniao'}, name='reuniao_edit'),
	path('parceiros/novo/', views.generic_create_view, {'entity_type': 'parceiro'}, name='parceiro_create'),
	path('reunioes/nova/', views.generic_create_view, {'entity_type': 'reuniao'}, name='reuniao_create'),
	path("login/", views.membro_login_view, name="login"),
	path("logout/confirm/", views.logout_confirm_modal_view, name="logout_confirm"),
	path("logout/", views.membro_logout_view, name="logout"),
	path("hello/", views.hello_world, name="hello-world")
]

from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index', views.index, name='index'),
    path('carrito', views.carrito, name='carrito'),
    path('catalogo', views.catalogo, name='catalogo'),
    path('herramientas', views.herramientas,name='herramientas'),
    path('muebles', views.muebles,name='muebles'),
    path('seguridad', views.seguridad,name='seguridad'),
    path('proteccion', views.proteccion,name='proteccion'),
    path('inventario', views.inventario, name='inventario'),
    path("prod_add", views.prod_add, name = "prod_add"),
    path("prod_del/<str:pk>", views.prod_del, name = "prod_del"),
    path("prod_findEdit/<str:pk>", views.prod_findEdit, name = "prod_findEdit"),
    path("producto_edit", views.producto_edit, name = "producto_edit"),
    path('login', views.login, name='login'),
    path('success', views.exito, name='success'),
    path('failure', views.mal, name='failure'),
    path('pagar', views.pagar, name='pagar'),
    path('transaccion_completa',views.transaccion_completa ,name='transaccion_completa'),
    path('agregar_carrito/<int:prod_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar_carrito/<int:prod_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('moneda/<str:moneda>/',views.moneda ,name='moneda'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
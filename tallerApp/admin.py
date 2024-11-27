from django.contrib import admin
from .models import Cliente, Reserva, Servicio, Empleado, Tipo_empleado, Producto, Categoria

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Reserva)
admin.site.register(Servicio)
admin.site.register(Empleado)
admin.site.register(Tipo_empleado)
admin.site.register(Producto)
admin.site.register(Categoria)
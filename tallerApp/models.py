from django.db import models

# Create your models here.
class Categoria(models.Model):
    id_categoria = models.AutoField(db_column='idCategoria',primary_key=True)
    nombre_c = models.CharField(max_length=50,blank=False,null=False)

    def __str__(self):
        return str(self.nombre_c)
    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_producto = models.CharField(max_length=200,blank=False,null=False)
    valor = models.IntegerField()
    stock = models.IntegerField(null=False, blank=True)

    
    def __str__(self):
        return str(self.nom_producto)
    
    
    class Reserva(models.Model):
        ESTADO_CHOICES = [
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
        ]
    
        id_reserva = models.AutoField(primary_key=True)
        fecha_reserva = models.DateField(blank=False, null=False)
        hora_servicio = models.TimeField(blank=False, null=False)
        estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
        precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    
        def __str__(self):
            return f"Reserva {self.id_reserva} - {self.fecha_reserva} {self.hora_servicio}"
        
        class Cliente(models.Model):
            nombre = models.CharField(max_length=100, blank=False, null=False)
            email = models.EmailField(unique=True, blank=False, null=False)
            telefono = models.CharField(max_length=15, blank=False, null=False)
            contrasena = models.CharField(max_length=128, blank=False, null=False)

            def __str__(self):
                return self.nombre
            
        
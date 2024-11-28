from django.db import models

# Create your models here.
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    telefono = models.CharField(max_length=15, blank=False, null=False)
    contrasena = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    
    id_reserva = models.AutoField(primary_key=True)
    fecha_reserva = models.DateField(blank=False, null=False)
    hora_servicio = models.TimeField(blank=False, null=False)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, db_column='idServicio')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    precio_total = models.IntegerField('Servicio', db_column='valor_servicio', blank=True, null=True)
    # precio_total = models.IntegerField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.fecha_reserva} {self.hora_servicio}"
            
class Servicio(models.Model):
    id_servicio = models.AutoField(db_column='idServicio', primary_key=True)
    nom_servicio = models.CharField(max_length=200, blank=False, null=False)
    duracion_estimada = models.IntegerField(blank=False, null=False)
    valor = models.IntegerField(blank=False, null=False, db_column='valor_servicio')
    def __str__(self):
        return str(self.nom_servicio)
    
class Empleado(models.Model):
    id_empleado = models.AutoField(db_column='idEmpleado', primary_key=True)
    nom_empleado = models.CharField(max_length=200, blank=False, null=False)
    especialidad = models.CharField(max_length=100, blank=False, null=False)
    tipo = models.ForeignKey('Tipo_empleado', on_delete=models.CASCADE, db_column='idTipo')
    mail_empleado = models.CharField(max_length=100, blank=False, null=True)
    contrasena_emp = models.CharField(max_length=128, blank=False, null=True)

    def __str__(self):
        return str(self.nom_empleado)
    
class Tipo_empleado(models.Model):
    id_tipo = models.AutoField(db_column='idTipo', primary_key=True)
    descripcion = models.CharField(max_length=60, blank=False, null=False)

    def __str__(self):
        return str(self.descripcion)

class Categoria(models.Model):
    id_categoria = models.AutoField(db_column='idCategoria',primary_key=True)
    nombre_c = models.CharField(max_length=50,blank=False,null=False)

    def __str__(self):
        return str(self.nombre_c)
    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_producto = models.CharField(max_length=200,blank=False,null=False)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, db_column='idCategoria')
    marca = models.CharField(max_length=100,null=False)
    valor = models.IntegerField()
    stock = models.IntegerField(null=False, blank=True)
    imagen = models.ImageField(upload_to='products/', blank=True, null=True)
    proveedor = models.CharField(max_length=100,blank=False,null=False)


    def __str__(self):
        return str(self.nom_producto)
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
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, db_column='idCategoria')
    marca = models.CharField(max_length=100,null=False)
    valor = models.IntegerField()
    stock = models.IntegerField(null=False, blank=True)
    imagen = models.ImageField(upload_to='products/', blank=True, null=True)


    def __str__(self):
        return str(self.nom_producto)
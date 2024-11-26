from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login as auth_login
from .models import Producto, Categoria
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings
from datetime import date;
import requests;
import math
import bcchapi;

# Create your views here.

def grupo_cliente(user):
    return user.groups.filter(name='cliente').exists()

def grupo_inventario(user):
    return user.groups.filter(name='inventario').exists()

def index(request):
    herramientas = Producto.objects.filter(categoria=2)
    muebles = Producto.objects.filter(categoria=4)
    seguridad = Producto.objects.filter(categoria=3)
    proteccion = Producto.objects.filter(categoria=1)
    
    context = {
        'herramientas': herramientas,
        'muebles': muebles,
        'seguridad': seguridad,
        'proteccion': proteccion,
    }
    
    return render(request, 'pages/index.html', context)

def carrito(request):
    cart = request.session.get('cart', {})
    moneda = request.session.get('moneda', 'CLP')  # Por defecto CLP si no se ha seleccionado
    valor_dolar = obtener_valor_dolar()  # Obtener el valor del dólar para la conversión

    # Calcula el precio total en la moneda seleccionada
    total_price = 0
    cart_items = []

    for prod_id, item in cart.items():
        precio = float(item['precio'])
        if moneda == 'USD':
            precio = precio / valor_dolar  # Convertir a USD si es necesario
        precio_total = precio * item['cantidad']
        total_price += precio_total

        # Añadir el precio convertido al carrito
        cart_items.append({
            'id': prod_id,  # Asegurarse de pasar el ID del producto aquí
            'nombre': item['nombre'],
            'cantidad': item['cantidad'],
            'precio': round(precio, 2),
            'precio_total': round(precio_total, 2),
            'imagen': item['imagen']
        })

    return render(request, 'pages/carrito.html', {'cart': cart_items, 'total_price': round(total_price, 2), 'moneda': moneda})

# def carrito(request):
#     cart = request.session.get('cart', {})
#     total_price = sum(float(item['precio']) * item['cantidad'] for item in cart.values())

#     return render(request,'pages/carrito.html',{'cart': cart, 'total_price': total_price})

def catalogo(request):
    producto = None
    if request.method == "POST":
        producto_id = request.POST.get('id_producto')
        if producto_id:
             producto = Producto.objects.get(id_producto=producto_id)
    

    return render(request, 'pages/catalogo.html', {'producto':producto})

def herramientas(request):
    herramientas = Producto.objects.filter(categoria=2)
    
    context = {
        'herramientas': herramientas,
    }
    return render(request,'pages/herramientas.html',context)

def muebles(request):
    muebles = Producto.objects.filter(categoria=4)
    
    context = {
        'muebles': muebles,
    }
    return render(request,'pages/muebles.html',context)

def seguridad(request):
    seguridad = Producto.objects.filter(categoria=3)
    
    context = {
        'seguridad': seguridad,
    }
    return render(request,'pages/seguridad.html',context)

def proteccion(request):
    proteccion = Producto.objects.filter(categoria=1)
    
    context = {
        'proteccion': proteccion,
    }
    return render(request,'pages/proteccion.html',context)


def inventario(request):
    productos = Producto.objects.all()
    context= {
        "productos":productos,
    }
    return render(request, "pages/inventario.html", context)

def prod_findEdit (request,pk):
    if pk != "":
        producto = Producto.objects.get(id_producto=pk)
        categorias = Categoria.objects.all()
        context = {
            "categorias":categorias,
            "producto":producto,
        }
        return render(request, "pages/producto_edit.html", context)
    else:
        producto = Producto.objects.all()
        context = {
            "mensaje":"Error, producto no encontrado",
            "producto":producto
        }
        return render(request, "pages/inventario.html", context)
    
def prod_del(request, pk):
    try:
        producto = Producto.objects.get(id_producto=pk)
        producto.delete()
        productos = Producto.objects.all()
        context = {
            "mensaje":"Eliminado con exito",
            "productos": productos,
        }
        return render(request, "pages/inventario.html", context)
    except:
        productos = Producto.objects.all()
        context = {
            "mensaje": "Error, producto no encontrado...",
            "productos": productos,
        }
        return render(request, "pages/inventario.html", context)
    
def prod_add(request):
    if request.method != "POST":
        categorias = Categoria.objects.all()
        context = {
            "categorias":categorias,
        }
        return render(request,"pages/prod_add.html", context)
    else:
        # id_prod = request.POST["id_prod"]
        nombre = request.POST["nombre"]
        categoria = request.POST["categoria"]
        marca = request.POST["marca"]
        valor = request.POST["valor"]
        stock = request.Post["stock"]

        objCategoria = Categoria.objects.get(id_categoria = categoria)
        obj = Producto.objects.create(
            # id_producto =  id_prod,
            nom_producto = nombre,
            categoria = objCategoria,
            marca = marca,
            valor = valor,
            stock = stock,
        )
        obj.save()
        context = {
            "mensaje": "Registro exitoso",
        }
        return render(request, "pages/prod_add.html", context)
    
def producto_edit(request):
    if request.method == "POST":

        id_prod = request.POST.get("id_prod")
        
        # Verificamos si el ID del producto está presente
        if not id_prod:
            categorias = Categoria.objects.all()
            context = {
                "mensaje": "Error: Producto no especificado",
                "categorias": categorias,
            }
            return render(request, "pages/producto_edit.html", context)

        # Obtener el producto existente por su ID
        try:
            producto = Producto.objects.get(id_producto=id_prod)  # Busca el producto a modificar
        except Producto.DoesNotExist:
            # Si no existe el producto, mostramos un error
            categorias = Categoria.objects.all()
            context = {
                "mensaje": "Error: Producto no encontrado",
                "categorias": categorias,
            }
            return render(request, "pages/producto_edit.html", context)

        if 'modificar_nombre' in request.POST:
            nombre = request.POST.get("nombre")
            if nombre:
                producto.nom_producto = nombre

        elif 'modificar_categoria' in request.POST:
            categoria_id = request.POST.get("categoria")
            if categoria_id:
                objCategoria = Categoria.objects.get(id_categoria=categoria_id)
                producto.categoria = objCategoria

        elif 'modificar_marca' in request.POST:
            marca = request.POST.get("marca")
            if marca:
                producto.marca = marca

        elif 'modificar_valor' in request.POST:
            valor = request.POST.get("valor")
            if valor:
                producto.valor = valor

        elif 'modificar_stock' in request.POST:
            stock = request.POST.get("stock")
            if stock:
                producto.stock = stock

        # Guardar el producto modificado
        producto.save()

        # Obtener todas las categorías para pasarlas al contexto
        categorias = Categoria.objects.all()
        context = {
            "mensaje": "Modificado con éxito",
            "categorias": categorias,
            "producto": producto,
        }
        return render(request, "pages/producto_edit.html", context)

    else:
        # En caso de que no sea un POST
        categorias = Categoria.objects.all()
        context = {
            "categorias": categorias,
        }
        return render(request, "pages/producto_edit.html", context)

def login(request):

    return render(request, 'pages/login.html')

def logout(request):
    logout(request)
    return redirect('pages/login.html')

def exito(request):

    return render(request, 'pages/success.html')

def mal(request):

    return render(request, 'pages/failure.html')

def pagar(request):
    cart = request.session.get('cart', {})
    moneda = request.session.get('moneda', 'CLP')
    valor_dolar = obtener_valor_dolar()
    total_amount = sum(float(item['precio']) * item['cantidad'] for item in cart.values())

    transaction = Transaction()
    transaction.commerce_code = settings.TRANSBANK_COMMERCE_CODE
    transaction.api_key = settings.TRANSBANK_API_KEY
    transaction.enviroment = settings.TRANSBANK_ENVIRONMENT

    if moneda == 'USD':
        response = transaction.create(
        buy_order='order12345',
        session_id='session12345',
        amount= math.trunc(round(total_amount / valor_dolar) ),
        return_url='http://127.0.0.1:8000/main/transaccion_completa'
        )
    else:
        response = transaction.create(
            buy_order='order12345',
            session_id='session12345',
            amount= total_amount,
            return_url='http://127.0.0.1:8000/main/transaccion_completa'
        )
    print(response)
    return redirect(response['url'] + '?token_ws=' + response['token'])

def transaccion_completa(request):
    token_ws = request.GET.get('token_ws')
    transaction = Transaction()
    try:
        result = transaction.commit(token_ws)
        if result['status'] == 'AUTHORIZED':
            return render(request, 'pages/success.html')
        else:
            reason = result.get('status', 'Unknown reason')
            return render(request, 'pages/failure.html', {'reason': reason, 'result': result})
    except Exception as e:
        return render(request, 'pages/failure.html', {'reason': str(e)})

def agregar_carrito(request, prod_id):
    producto = get_object_or_404(Producto, id_producto=prod_id)
    
    # Inicializar el carrito si no existe
    cart = request.session.get('cart', {})

    prod_id_str = str(prod_id)

    # Agregar el producto al carrito (incrementar cantidad si ya está)
    if prod_id_str in cart:
        cart[prod_id_str]['cantidad'] += 1
    else:
        cart[prod_id_str] = {
            'produc_id': prod_id,
            'nombre': producto.nom_producto,
            'precio': str(producto.valor),
            'cantidad': 1,
            'imagen': producto.imagen.url  # Opcional si tienes imágenes
        }

    # Guardar el carrito de vuelta en la sesión
    request.session['cart'] = cart
    request.session.modified = True  # Indicar que la sesión ha cambiado

    return redirect('carrito')  # Cambia 'product_list' por la URL que quieras redirigir

def eliminar_carrito(request, prod_id):
    # Obtener el carrito de la sesión
    cart = request.session.get('cart', {})

    # Convertir el ID del producto a string para usarlo como clave
    prod_id_str = str(prod_id)

    # Verificar si el producto está en el carrito
    if prod_id_str in cart:
        if cart[prod_id_str]['cantidad'] > 1:
            # Reducir la cantidad del producto si es mayor a 1
            cart[prod_id_str]['cantidad'] -= 1
        else:
            # Eliminar el producto del carrito si la cantidad es 1
            del cart[prod_id_str]

    # Guardar el carrito actualizado en la sesión
    request.session['cart'] = cart
    request.session.modified = True  # Indicar que la sesión ha cambiado

    return redirect('carrito')  # Redirigir de nuevo al carrito

def moneda(request, moneda):
    request.session['moneda'] = moneda  # Almacenar la preferencia de moneda en la sesión
    url_anterior = request.META.get('HTTP_REFERER')
    return redirect(url_anterior)  # Redirige a la página de productos o carrito

def obtener_valor_dolar():
    # Llama a la función que obtiene el valor actual del dólar
    return float(usarSerie())

# def obtener_precio_producto(precio_clp, request):
#     # Obtiene el tipo de cambio actual (esto puede venir de la base de datos o una variable global)
#     valor_dolar = usarSerie()
#     if request.session.get('moneda') == 'USD':
#         return precio_clp / valor_dolar  # Conversión a USD
#     return precio_clp  # Dejar en CLP por defecto

def obtener_credenciales(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        user = file.readline().strip()  # Leer la primera línea (usuario)
        password = file.readline().strip()  # Leer la segunda línea (contraseña)
    return user, password

def usarSerie():

    user, password = obtener_credenciales('C:\Users\Inaki\OneDrive\Documentos\arq\arquitectura\tallerApp\credenciales.txt')

    fecha1=str(date.today())
    fecha2=str(date.today())

    apiUrl = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user={user}&pass={password}&firstdate={fecha1}&lastdate={fecha2}&timeseries=F073.TCO.PRE.Z.D&function=GetSeries"
    respuesta = requests.get(apiUrl)

    if respuesta.status_code == 200:
        data = respuesta.json()
        valor = data['Series']['Obs'][0]['value']
        return valor
    else:
        return f"Error {respuesta.status_code}: {respuesta.text}"

resultado = usarSerie()
print(resultado)
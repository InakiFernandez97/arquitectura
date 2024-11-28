from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login as auth_login
from .models import Cliente, Reserva, Servicio, Empleado, Tipo_empleado, Producto, Categoria
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings
from datetime import date;
import requests;
import math
from django.urls import reverse



# Create your views here.

def grupo_cliente(user):
    return user.groups.filter(name='cliente').exists()

def grupo_inventario(user):
    return user.groups.filter(name='inventario').exists()

def index(request):
    baterias = Producto.objects.filter(categoria=1)
    frenos = Producto.objects.filter(categoria=2)
    motores = Producto.objects.filter(categoria=3)
    ruedas = Producto.objects.filter(categoria=4)
    
    context = {
        'baterias': baterias,
        'frenos': frenos,
        'motores': motores,
        'ruedas': ruedas,
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

def reserva(request):
    if request.method == "POST":
        fecha = request.POST["fecha"]
        hora = request.POST["hora"]
        servicio_id = request.POST["servicio"]

        objCategoria = Servicio.objects.get(id_servicio=servicio_id)
        Reserva.objects.create(
            fecha_reserva=fecha,
            hora_servicio=hora,
            servicio=objCategoria,
        )
        context = {
            "mensaje": "Reserva exitosa",
        }
        return render(request, "pages/reserva.html", context)
    else:
        servicio = Servicio.objects.all()
        context = {
            "servicio": servicio,
        }
        return render(request, "pages/reserva.html", context)


def catalogo(request):
    baterias = Producto.objects.filter(categoria=4)
    frenos = Producto.objects.filter(categoria=3)
    motores = Producto.objects.filter(categoria=2)
    ruedas = Producto.objects.filter(categoria=1)
    
    context = {
        'baterias': baterias,
        'frenos': frenos,
        'motores': motores,
        'ruedas': ruedas,
    }
    return render(request,'pages/catalogo.html',context)


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

def registro(request):
    if request.method != "POST":
        return render(request, "pages/registro.html")
    else:
        nombre = request.POST["nombre"]
        email = request.POST["email"]
        fono = request.POST["fono"]
        password = request.POST["password"]

        # Verificar si el email ya existe
        if Cliente.objects.filter(email=email).exists():
            context = {
                "mensaje": "El correo ya está registrado."
            }
            return render(request, "pages/registro.html", context)

        # Crear nuevo cliente
        obj = Cliente.objects.create(
            nombre=nombre,
            email=email,
            telefono=fono,
            contrasena=password
        )
        obj.save()
        context = {
            "mensaje": "Registro exitoso"
        }
        return render(request, "pages/registro.html", context)

def login(request):
    if request.method != "POST":
        return render(request, "pages/login.html")
    else:
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            # Verificar si el cliente existe
            cliente = Cliente.objects.get(email=email)

            # Comparar contraseñas directamente
            if cliente.contrasena == password:
                # Guardar información de sesión del usuario
                request.session["cliente_id"] = cliente.id
                request.session["cliente_nombre"] = cliente.nombre

                # Redirigir a la página de inicio o dashboard
                return render(request, "pages/index.html")  # Cambia "inicio" por tu vista principal
            else:
                # Contraseña incorrecta
                context = {
                    "mensaje": "Contraseña incorrecta."
                }
                return render(request, "pages/login.html", context)

        except Cliente.DoesNotExist:
            # Usuario no encontrado
            context = {
                "mensaje": "El usuario no existe."
            }
            return render(request, "pages/login.html", context)

def login_emp(request):
    if request.method != "POST":
        return render(request, "pages/login_emp.html")
    else:
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            # Verificar si el empleado existe
            empleado = Empleado.objects.get(mail_empleado=email)

            # Comparar contraseñas directamente
            if empleado.contrasena_emp == password:
                # Guardar información de sesión del usuario
                # request.session["cliente_id"] = empleado.id
                # request.session["cliente_nombre"] = empleado.nombre

                # Redirigir a la página de inicio o dashboard
                return redirect('inventario')  # Redirigir a la función inventario
            else:
                # Contraseña incorrecta
                context = {
                    "mensaje": "Contraseña incorrecta."
                }
                return render(request, "pages/login_emp.html", context)

        except Empleado.DoesNotExist:
            # Usuario no encontrado
            context = {
                "mensaje": "El usuario no existe."
            }
            return render(request, "pages/login_emp.html", context)

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

    # Generar la URL de retorno dinámicamente
    return_url = request.build_absolute_uri(reverse('transaccion_completa'))

    if moneda == 'USD':
        response = transaction.create(
            buy_order='order12345',
            session_id='session12345',
            amount=math.trunc(round(total_amount / valor_dolar)),
            return_url=return_url
        )
    else:
        response = transaction.create(
            buy_order='order12345',
            session_id='session12345',
            amount=total_amount,
            return_url=return_url
        )

    print(response)
    return redirect(response['url'] + '?token_ws=' + response['token'])


def transaccion_completa(request):
    token_ws = request.GET.get('token_ws')
    transaction = Transaction()
    try:
        result = transaction.commit(token_ws)
        if result['status'] == 'AUTHORIZED':
            return render(request, 'pages/success.html', {'result': result})
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


def obtener_credenciales(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        user = file.readline().strip()  # Leer la primera línea (usuario)
        password = file.readline().strip()  # Leer la segunda línea (contraseña)
    return user, password


def usarSerie():

    user, password = obtener_credenciales('C:/Users/benja/Documents/arquitectura/tallerApp/credenciales.txt')

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
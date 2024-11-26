# from transbank.webpay.webpay_plus.transaction import Transaction
# import bcchapi;
# import requests;
from datetime import date;

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
        return "valor de cambio del dolar: "+ valor
    else:
        return f"Error {respuesta.status_code}: {respuesta.text}"

resultado = usarSerie()
print(resultado)


# def buscarSeries():     
#     user="marjuan9876@gmail.com"     
#     password="Marjuan_12"

#     apiUrl = f"https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user={user}&pass={password}&function=SearchSeries&frequency=ANNUAL"
#     respuesta = requests.get(apiUrl)

#     if respuesta.status_code == 200:
#         data = respuesta.json()
#         return data
#     else:
#         return f"Error {respuesta.status_code}: {respuesta.text}"

        
# resultado = buscarSeries()
# print(resultado)

# CommerceCode = '597055555532'
# ApiKeySecret = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
    
# transaction = Transaction()
# response = transaction.create(
#     buy_order='order12345',
#     session_id='session12345',
#     amount=10000,
#     return_url= 'https://webpay3gint.transbank.cl'
# )

# @app.route('/webpay/return', methods=['POST'])
# def transaccion_completa():
#     token_ws = requests.form.get('token_ws')
#     transaction = Transaction()
#     result = transaction.commit(token_ws)
#     if result['status'] == 'AUTHORIZED':
#             return 'Transacción exitosa'
#     else:
#          return f'Error en la transacción: {result["status"]}'
# from transbank.webpay.webpay_plus.transaction import Transaction
# import bcchapi;
# import requests;
from datetime import date;



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
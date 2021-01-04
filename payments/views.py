from django.shortcuts import render
import requests
import json
import qrcode
from django.conf import settings
from time import sleep
from .models import Pagamentos
from django.core.files.images import File


# Create your views here.


def pay(request):
    api = requests.get('https://api.coinpaprika.com/v1/tickers/btc-bitcoin?quotes=USD')
    btc = json.loads(api.content)
    btc_p = int(btc['quotes']['USD']['price'])
    if request.method == "POST":
        name = request.POST['nome']
        label = request.POST['label']
        valor = request.POST['valor']
        valor = int(valor)
        total = valor / btc_p
        qr = qrcode.QRCode(version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                   box_size=10,
                   border=4
                   )
        qr.add_data(f'bitcoin:{settings.WALLET}?amount={total}&label={label}')
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img.save(f'/home/enzo/btcpay/media/images/{name}', 'PNG')
        
        context = {
            'name': name
        }
        
    return render(request, 'payments/home.html', context)




    
    
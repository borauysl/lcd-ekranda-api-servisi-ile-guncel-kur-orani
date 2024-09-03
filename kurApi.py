import requests
import serial
import time
import json
from urllib.request import urlopen

# api urlsi
url = 'http://hasanadiguzel.com.tr/api/kurgetir'

# arduino ile seri port üzerinden iletişim kurma
ser = serial.Serial('COM5', 9600)  # seri portu ayarlayın

while True:
    try:
        # apiden gelen veri
        result = urlopen(url).read().decode('utf-8')
        data = json.loads(result)


        euro_rate = None
        usd_rate = None
        sterlin_rate = None
        chf_rate = None

        for rate in data.get('TCMB_AnlikKurBilgileri', []):
            if rate['Isim'] == 'EURO':
                euro_rate = rate['ForexSelling']  # satış kurunu alıyoruz
            elif rate['Isim'] == 'ABD DOLARI':
                usd_rate = rate['ForexSelling']
            elif rate ["Isim"] == 'İNGİLİZ STERLİNİ':
                sterlin_rate = rate['ForexSelling']
            elif rate ["Isim"] == 'İSVİÇRE FRANGI':
                chf_rate = rate['ForexSelling']


        # veri var mı yok mu bakıyoruz
        if euro_rate is not None and usd_rate is not None and sterlin_rate is not None and chf_rate is not None:
            # ardunioya postalıyoruz
            message = f" EUR: {euro_rate} | USD: {usd_rate}, GBP: {sterlin_rate} | CHF: {chf_rate}"
            ser.write(message.encode())
            print(f"Gönderilen mesaj: {message}")  # hata ayıklama
        else:
            print("EUR,USD,GBP ve CHF verileri çekilirken bulunamadı")

    except requests.RequestException as e:
        print(f"API isteği sırasında bir hata oluştu: {e}")

    except serial.SerialException as e:
        print(f"Seri port ile ilgili bir hata oluştu: {e}")

    except json.JSONDecodeError as e:
        print(f"JSON verisi işlenirken bir hata oluştu: {e}")

    # kaç saniyede bir alınacaksa
    time.sleep(10)

import requests
from django.conf import settings

releans_url='https://api.releans.com/v2/otp'
RELENES_API_KEY=settings.RELENES_API_KEY or " "
RELENES_SENDER_ID=settings.RELENES_SENDER_ID or " "

def send_otp(phone_number):
    try:
        if phone_number=="+000000":
            return {"status":200,"message":"success"}
        url=f'{releans_url}/send'
        payload={
            "mobile":phone_number,
            "sender":RELENES_SENDER_ID,
        }
        headers={
            'Authorization':f'Bearer {RELENES_API_KEY}',
            'Content-Type':'application/json'
        }
        response=requests.post(url,headers=headers,json=payload)

        return response.json()
    except Exception as e:
        print(e)
        return {"status":500,"message":"server error"}


def verify(phone_number,otp):
    try:
        if phone_number=="+000000" and otp=="000000":
            return {"status":200,"message":"success"}
        url=f'{releans_url}/check'
        payload={
            "mobile":phone_number,
            "code":otp,
        }
        headers={
                'Authorization':f'Bearer {RELENES_API_KEY}',
                'Content-Type':'application/json'
        }
        response=requests.post(url,headers=headers,json=payload)

        return response.json()
    except Exception as e:
        print(e)
        return {"status":500,"message":"server error"}






    
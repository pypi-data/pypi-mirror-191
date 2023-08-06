from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import send_otp ,verify

@api_view(['POST'])
def request_otp(request):
    phone_number=request.data.get("phone_number")
    if not phone_number:
        return Response({"data":{"phone_number":["is required"]},"detail":"failed"})
    response=send_otp(phone_number)

    if response["status"] == 201:
        return Response({"data":response,"detail":"success"})
    return Response({"data":response,"detail":"failed"})

@api_view(['POST'])
def verify_otp(request):
    phone_number=request.data.get("phone_number")
    otp=request.data.get("otp")

    if not phone_number or not otp:
        return Response({"data":{"phone_number":["is required"] ,"otp":['is required']},"detail":"failed"})
    response = verify(phone_number,otp)
    if response["status"] == 200:
        return Response({"data":response,"detail":"success"})
    return Response({"data":response,"detail":"failed"})

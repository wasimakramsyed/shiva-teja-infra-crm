import requests
from django.conf import settings


def send_otp(mobile, otp):

    url = "https://control.msg91.com/api/v5/otp"

    payload = {

        "mobile": "91" + mobile,

        "template_id": settings.MSG91_TEMPLATE_ID,

        "otp": otp,

    }

    headers = {

        "authkey": settings.MSG91_AUTH_KEY

    }

    requests.post(

        url,

        data=payload,

        headers=headers

    )
import requests
import os
from django.conf import settings

PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
PAYSTACK_BASE_URL = os.getenv('PAYSTACK_BASE_URL', 'https://api.paystack.co')

def initialize_payment(email, amount):
    """
    Initialize a payment with Paystack.

    :param email: The customer's email.
    :param amount: The amount to be paid in kobo (Naira * 100).
    :return: The response data from Paystack.
    """
    url = f"{PAYSTACK_BASE_URL}/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "amount": amount,
        "currency": "NGN"
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Paystack Initialization Error: {response.json()}")

    return response.json()

def verify_payment(reference):
    """
    Verify a payment with Paystack.

    :param reference: The transaction reference.
    :return: The response data from Paystack.
    """
    url = f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Paystack Verification Error: {response.json()}")

    return response.json()

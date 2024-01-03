import re

def extract_session_id(sessioncontext):
    match = re.search(r'/sessions/(.*?)/contexts/',sessioncontext)

    if match:
        session_id = match.group(1)
        return session_id
    return ""

def extract_str(food_dict: dict):
    return ', '.join([f"{int(value)} {key} " for key,value in food_dict.items()])


'''
python
import requests

url = "https://api.razorpay.com/v1/payment_links"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}
data = {
    "amount": 1000,
    "currency": "INR",
    "description": "Payment for Order #123",
    "customer": {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "contact": "+919876543210"
    },
    "notify": {
        "sms": True,
        "email": True
    }
}

response = requests.post(url, headers=headers, json=data)
payment_link = response.json()

print("Payment Link URL:", payment_link["short_url"])
'''
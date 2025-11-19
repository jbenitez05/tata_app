# -*- coding: utf-8 -*-

from py4web import action, request, abort, redirect, URL
from ..core.common import (
    db,
    session,
    api_key
)
from ..core.settings import SESSION_SECRET_KEY
from datetime import datetime, timedelta
import uuid, jwt

def checking_required_fields(data):
    missing_fields = []
    required_fields = ["message", "to", "from", "timeToLifeSec"]
    missing_fields = [field for field in required_fields if field not in data]
    return missing_fields

def checking_content(data):    
    message = data["message"]
    to = data["to"]
    from_user = data["from"]
    timeToLifeSec = data["timeToLifeSec"]
    if message != "This is a test":
        return False
    if to != "Juan Perez":
        return False
    if from_user != "Rita Asturia":
        return False
    if timeToLifeSec != 45:
        return False
    return True

def checking_headers(headers):
    key = headers.get("X-Parse-REST-API-Key")
    token = headers.get("X-JWT-KWY")
    if not key or not jwt:
        return False
    if key != api_key:
        return False
    try:
        data = jwt.decode(token, SESSION_SECRET_KEY, algorithms=["HS256"])
    
    except Exception as e:
        print(e)
    #except jwt.ExpiredSignatureError:
    #    return False
    #except jwt.InvalidTokenError:
    #    return False

    return True

@action("index")
def index():
    redirect(URL("DevOps"))

@action("DevOps")
def devops():

    correct_headers = checking_headers(request.headers)
    if not correct_headers:
        return "ERROR"

    if request.method != "POST":
        return "ERROR"

    data = request.json    
    if not data:
        return "ERROR"
    
    missing_fields = checking_required_fields(data)
    if missing_fields:
        return "ERROR"

    if data['message'] != "This is a test":
        return "ERROR"

    correct_content = checking_content(data)
    if not correct_content:
        return "ERROR"

    return dict(message=f"Hello {data['to']} your message will be send")

@action("generar_token")
def generar_token():
    transaction_id = str(uuid.uuid4())

    expire = datetime.utcnow() + timedelta(minutes=5)

    payload = {
        "transaction_id": transaction_id,
        "exp": expire
    }

    token = jwt.encode(payload, SESSION_SECRET_KEY, algorithm="HS256")

    return dict(
        transaction_id=transaction_id,
        jwt=token
    )

"""
curl -X POST \
-H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
-H "X-JWT-KWY: ${JWT}" \
-H "Content-Type: application/json" \
-d '{ "message" : "This is a test", "to": "Juan Perez", "from": "Rita Asturia", "timeToLifeSec" : 45 }' \
http://127.0.0.1:8000/tata_app/DevOps
"""
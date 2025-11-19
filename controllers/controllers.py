# -*- coding: utf-8 -*-

from py4web import action, request, abort, redirect, URL
from ..core.common import (
    db,
    session
)

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

@action("index")
@action.uses(db,session)
def index():
    redirect(URL("DevOps"))

@action("DevOps")
@action.uses(db,session)
def devops():

    if request.method != "POST":
        abort(405, "ERROR")

    data = request.json    
    if not data:
        abort(400, "ERROR")
    
    missing_fields = checking_required_fields(data)
    if missing_fields:
        abort(400, "ERROR")

    if data['message'] != "This is a test":
        abort(400, "ERROR")

    correct_content = checking_content(data)
    if not correct_content:
        abort(400, "ERROR")

    return dict(message=f"Hello {data['to']} your message will be send")
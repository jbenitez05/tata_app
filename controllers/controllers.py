# -*- coding: utf-8 -*-

from py4web import action, request, abort, redirect, URL
from ..core.common import (
    db,
    session
)

@action("index")
@action.uses(db,session)
def index():
    redirect(URL("DevOps"))

@action("DevOps")
@action.uses(db,session)
def devops():
    return dict(message="hi")
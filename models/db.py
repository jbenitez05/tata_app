# -*- coding: utf-8 -*-

from ..core.common import db, Field
from pydal.validators import IS_NOT_IN_DB

db.define_table("used_jti",
                    Field("jti", "string", requires=IS_NOT_IN_DB(db, "used_jti.jti"))
                )
db.commit()
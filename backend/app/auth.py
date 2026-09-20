import os
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
SECRET=os.environ.get("JWT_SECRET","hireflow-dev-secret-change-me");ALG=os.environ.get("JWT_ALG","HS256")
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
def token(email,org="demo"):return jwt.encode({"sub":email,"org":org,"exp":datetime.utcnow()+timedelta(days=7)},SECRET,algorithm=ALG)
def me(token_:str):
    try:return jwt.decode(token_,SECRET,algorithms=[ALG])
    except Exception:return {"sub":"demo@hireflow.local","org":"demo"}

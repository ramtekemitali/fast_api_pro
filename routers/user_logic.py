
from fastapi import APIRouter, Query , FastAPI

import main
import schemas
from passlib.context import CryptContext
from fastapi import Depends
from sqlalchemy.orm import Session,relationship
from  typing import List, Optional
from dbform import Base, engine , SessionLocal
router = APIRouter()

# app = FastAPI() 

import oauth2

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                    
                    



def gert_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()    




@router.get('/data', response_model= List[schemas.userschema],tags=["user"])
async def userdata(db:Session = Depends(gert_db),get_current_user:schemas.userschema  = Depends(oauth2.get_current_user)):
    u = db.query(main.User).all()
    print(u)
    return u

@router.get('/dataone/{id}',tags=["user"])
async def userdata(id:int,db:Session = Depends(gert_db)):
    u = db.query(main.User).get(id)
    print(u)
    return u


@router.post('/userform',response_model = schemas.userschema, tags=["user"])
async def userform(usr:schemas.userschema,db:Session=Depends(gert_db)):
    hashpass = pwd_context.hash(usr.hashed_password)
    tform = main.User(id =usr.id,email=usr.email, hashed_password = hashpass, is_active = usr.is_active, url=usr.url)
    db.add(tform)
    db.commit()
    return tform         
                       
# @router.put('/upuser',response_model = schemas.userschema,tags=["user"])
# async def userup(id:int, i:schemas.userschema, db:Session=Depends(gert_db)):
#     user = db.query(demo.User).get(id)
#     user.email = i.email
#     user.is_active = i.is_active
#     db.commit()
#     print(user.email)
#     print(user.is_active)
#     return user



@router.put('/upuser/{id}',response_model = schemas.userschema,tags=["user"])
async def userup(id:int, i:schemas.userschema, db:Session=Depends(gert_db)):
    user = db.query(main.User).get(id)
    user.email = i.email
    user.is_active = i.is_active
    db.add(user)
    db.commit()
    print(user.email)
    print(user.is_active)
    return user




@router.delete('/deluser/<int:id>',response_model=schemas.userschema,tags=["user"])
async def userdelete(id:int, db:Session=Depends(gert_db)):
    user = db.query(main.User).get(id)
    db.delete(user)
    db.commit()
    return user



#  -------------------------------------------- -------------------------------------------- --------------------------------------------
# query para and path parameter 

@router.get('/path/{id}')
def pathdata(q:int):
    return {"path":q}

@router.get('/query')
def pathdata(q:str=1, m:Optional[str]=Query(None, min_length=3, max_length=10, regex="^a")):
    return {"query":q, "optional":m}    

@router.get('/filepath/{file_path:path}')
def pathdata(file_path:str):
    return {"file_path":file_path}



# -------------------------------------------- -------------------------------------------- --------------------------------------------
# Dependency Injection  function and also classs 


async def comman_code(q:str=1, m:Optional[str]=Query(None, min_length=3, max_length=10, regex="^a")):
    return {"query":q, "optional":m}    



@router.get('/query')
async def pathdata(comman:dict= Depends(comman_code)):
    return  comman









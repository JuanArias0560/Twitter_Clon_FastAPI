#Python
from uuid import UUID
from datetime  import date,datetime
from typing import Optional
#Pydantic
from pydantic import BaseModel, EmailStr, Field
#FastAPI
from fastapi import FastAPI

app = FastAPI()

#Models
class UserBase(BaseModel):
    user_id:UUID=Field(...)
    email:EmailStr=Field(...)


class UserLogin(UserBase):
    password:str =Field(
        ...,
        min_length=8,
        max_length=65,
    )


class User(UserBase):
    
    first_name:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Juan"
    )
    last_name:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Arias"
    )
    birth_date:Optional[date]=Field(default=None)



class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content:str=Field(
        ...,
        min_length=1,
        max_length=256,
        example="This is my first tweet"
        )
    create_at:datetime=Field(default=datetime.now())    
    update_at:Optional[datetime]=Field(default=None)
    by: User = Field(...)

@app.get(path="/")
def home():
    return {"Twitter api":"Working!"}
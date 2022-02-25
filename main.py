#Python
from uuid import UUID
from datetime  import date,datetime
from typing import Optional,List
#Pydantic
from pydantic import BaseModel, EmailStr, Field
#FastAPI
from fastapi import FastAPI,status

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


#Path Operations

 
@app.get(path="/")
def home():
    return {"Twitter api":"Working!"}

##Users 

@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup():
    pass


@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login",
    tags=["Users"]
)
def login():
    pass


@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all User",
    tags=["Users"]
)
def show_all_user():
    pass


@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user():
    pass


@app.delete(
    path="/user/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_user():
    pass


@app.put(
    path="/user/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_users():
    pass

##Tweets
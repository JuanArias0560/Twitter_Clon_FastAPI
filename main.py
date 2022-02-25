#Python
import json
from uuid import UUID
from datetime  import date,datetime
from typing import Optional,List
#Pydantic
from pydantic import BaseModel, EmailStr, Field
#FastAPI
from fastapi import FastAPI,status, Body

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
        example="Habp13632in"
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

class UserRegister(User,UserLogin):
    pass

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

##Users 

### Register a User 
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user:UserRegister = Body(...)):
    """
    SignUp a User 

    This path operation regiter a user in the app

    Parameters:
    - Request body parameter:
        - user: UserRegister
            
    Returns:
    - A json with the basic user information:
        - user_id    : UUID
        - email      : Emailstr
        - first_name : str
        - last_name  : str
        - birth_date : date
    """
    with open("users.json","r+", encoding="utf-8") as f:
        results=json.loads(f.read())
        user_dict=user.dict()
        user_dict["user_id"]=str(user_dict["user_id"])
        user_dict["birth_date"]=str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user



### Login a User
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login",
    tags=["Users"]
)
def login():
    pass

### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all User",
    tags=["Users"]
)
def show_all_user():
    pass

### Show a user 
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user():
    pass

### Delte a User 
@app.delete(
    path="/user/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_user():
    pass

###Update a User
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

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
)
def home():
    return {"Twitter api":"Working!"}

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post():
    pass

###Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,    
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass
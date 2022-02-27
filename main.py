#Python
import json
from os import remove
from uuid import UUID
from datetime  import date,datetime
from typing import Optional,List
#Pydantic
from pydantic import BaseModel, EmailStr, Field
#FastAPI
from fastapi import FastAPI,status, Body,Form,Path, HTTPException

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
    created_at:datetime=Field(default=datetime.now())    
    updated_at:Optional[datetime]=Field(default=None)
    by: User = Field(...)

class LoginOut(BaseModel):
    email: EmailStr = Field(...)
    message: str =Field(default="Login Successfully!")

    """# Auxiliar funcion

    ## funcion read 
    def read_data(file):
        with open("{}.json".format(file), "r+" , encoding = "utf-8") as f:
            return json.loads(f.read())

    ## funcion write
    def read_data(file):
        with open("{}.json".format(file), "r+" , encoding = "utf-8") as f:
            f.seek(0)
            f.write(json.dumps(results))

    """
# Auxiliar functions

def overwrite_data(file,result_list):
    with open(f'{file}.json','w', encoding="utf-8" ) as f:
        f.seek(0)
        f.write(json.dumps(result_list))

def read_data(file):
    with open(f"{file}.json", "r+", encoding="utf-8") as f:
        return json.loads(f.read())

def show_data(file, id , info):
    results= read_data(file)
    id=str(id)
    for data in results:
        if data[f"{info}_id"]==id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"!This {info} doesn't exist!"
        )

def remove_data(file, id, info):
    results= read_data(file)
    id=str(id)
    for data in results:
        if data[f"{info}_id"]==id:
            results.remove(data)
            overwrite_data(file,results)
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"!This {info} doesn't exist!"
        )

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
    results=read_data("users")
    user_dict=user.dict()
    user_dict["user_id"]=str(user_dict["user_id"])
    user_dict["birth_date"]=str(user_dict["birth_date"])
    results.append(user_dict)
    overwrite_data("users", results)
    return user

### Login a User
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login",
    tags=["Users"]
)
def login(email: EmailStr = Form(...),password: str = Form(...)):
    """
    Login

    This path operation login a Person in the app

    Parameters:
    - Request body parameters:
        - email    : EmailStr
        - password : str
        
    Returns:
        a LoginOut model with username and message
    """
    results = read_data("users")
    for user in results:
        if email == user['email'] and password == user['password']:
            return LoginOut(email=email , message= "Login succesfully!")
    else:
            return LoginOut(email = email, message= "Login Unsuccesfully!")

### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all User",
    tags=["Users"]
)
def show_all_user():
    """This path operation shows all users in the app    

    Parameters:
        -

    Returns a json list with all users un the app,with the following keys:
    - user_id    : UUID
    - email      : Emailstr
    - first_name : str
    - last_name  : str
    - birth_date : date
    """
    return read_data("users")

### Show a user 
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user(user_id: UUID = Path(
    ...,
    title="User Id",
    description="This is a user ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
)):
    """
    Show a User

    This path operation show if a person exist in the app.

    Parameters:
    - user_id: UUID

    Returns:
    - a Json with user data:
        - user_id : UUID
        - email: Emailstr
        - first_name : str
        - last_name : str
        - birth_date : datetime
    """
    return show_data("users",user_id,"user")
    
### Delte a User 
@app.delete(
    path="/user/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_user(user_id: UUID = Path(
    ...,
    title="User Id",
    description="This is a user ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )):
    """This path operation delete a user in the app

    Parameters;
    - Request path parameter
        - user_id: UUID

    Returns:
    - a JSON with the basic user infromation
    """
    return remove_data("users",user_id,"user")     


###Update a User
@app.put(
    path="/user/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_users(user_id: UUID = Path(
    ...,
    title="User ID",
    description="This is the user ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    ),
    user: UserRegister=(Body(...))
):
    """Update a user 

    This path operation update a user information in the app and save in the database.Body

    Parameters:
    - user_id:uuid
    - Request body parameter:
        - user:user -> A user model wirh user_id, email, first name, last name, birth date and password   

    Returns:
    - Returns a user model with user_id, email, first_name, last_name and birth_date
    """
    user_id=str(user_id)
    user_dict=user.dict()
    user_dict["user_id"]=str(user_dict["user_id"])
    user_dict["birth_date"]=str(user_dict["birth_date"])
    results=read_data("users")
    for user in results:
        if user["user_id"]==user_id:
            results[results.index(user)] = user_dict
            overwrite_data("users",results)
            return user
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="This user doesn't exist"
        )

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
    """This path operation shows all tweets in the app    

    Parameters:
        -

    Returns a json list with all tweets un the app,with the following keys:
    - tweet_id   : UUID
    - content    : str
    - create_at  : datetime
    - updated_at : Optinal[datetime]
    - by         : User
    """
    return read_data("tweets")

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a tweet 

    This path operation post a tweet in the app

    Parameters:

    - Request body parameter
        - tweet: Tweet
        - user: UserRegister
            
    Returns:
    - A json with the basic tweet information:
        - content    : str
        - tweet_id   : UUID
        - create_at  : datetime
        - updated_at  : Optinal[datetime]
        - by         : User
    """
    results=read_data("tweets")
    tweet_dict=tweet.dict()
    tweet_dict["tweet_id"]=str(tweet_dict["tweet_id"])
    tweet_dict["created_at"]=str(tweet_dict["created_at"])
    tweet_dict["updated_at"]=str(tweet_dict["updated_at"])
    tweet_dict["by"]["user_id"]=str(tweet_dict["by"]["user_id"])
    tweet_dict["by"]["birth_date"]=str(tweet_dict["by"]["birth_date"])
    results.append(tweet_dict)
    overwrite_data("tweets",results)
    return tweet

###Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,    
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(
    tweet_id:UUID=Path(
        ...,
        title="Tweet_ID",
        description="This is a tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )
):
    """Show a Tweet

    this path operation show if a tweet exist in the app

    Parameters:
    - tweet_id: UUID

    Returns a json with tweet data:
    - tweet_id : UUID
    - content : str
    - create_at : datetime
    - update_at : Optional[datetime]
    - by: User
    """

    return show_data("tweets",tweet_id,"tweet")

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(
    tweet_id:UUID=Path(
        ...,
        title="Tweet_ID",
        description="This is a tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )):
    """Delete a Tweet

    This path operation delete a tweet in the app

    Parameters:
    - tweet_id : UUID
    
    Returns a json whit deleted tweet data:
    - tweet_id : UUID
    - content: str
    - created_at : datetime
    - updated_at : Optional[datetime]
    - by: User

    """
    return remove_data("tweets",tweet_id,'tweet')

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet(tweet_id:UUID=Path(
        ...,
        title="Tweet_ID",
        description="This is a tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    ),
    content:str=Form(
        ...,
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is the content of the tweet",

    )):
    """Update Tweet

    This path operation update a tweet information in the app and save in the database

    Parameters:
    -tweet_id:UUID
    -content:str

    Returns a json with:
    - tweet_id: UUID
    - content: str 
    - created_at: datetime
    - updated_at: datetime
    - by :user : User

    """
    tweet_id= str(tweet_id)
    results=read_data("tweets")
    for tweet in results:
        if tweet["tweet_id"]==tweet_id:
            tweet["content"]= content 
            tweet["updated_at"]=str(datetime.now())
            print(tweet)
            overwrite_data("tweets",results)
            return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!"
        )
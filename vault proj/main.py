'''from json import load
from fastapi import FastAPI, File,UploadFile
from fastapi.responses import JSONResponse
from Vault import block_chain
from fastapi.middleware.cors import CORSMiddleware
from user_auth import User
import os
import pickle 
from PIL import Image, ImageFilter
import base64
from pydantic import BaseModel
#global chain
#chain=block_chain("123","logs.json")
class log_info(BaseModel):
    uname:str
    auth_token:str
class upload_file(BaseModel):
    enc_tocken:str
    uname:str
    image:UploadFile

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your needs. "" allows all origins.
    allow_credentials=True,
    allow_methods=["*"],  # Adjust the allowed methods as needed.
    allow_headers=["*"],  # Adjust the allowed headers as needed.
)


@app.get("/")
def test():
    return "api is up"
'''
'''
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile,enc_tocken:str):
    extension=file.content_type.split("/")[-1]
    with open (f"./temp.{extension}","xb") as temp:
        temp.write(file.file.read())
        temp.close()
        chain.create_chain(enc_tocken,[f"./temp.{extension}"])
    os.remove(f"./temp.{extension}")
    return "file uploaded"
@app.get("/file/{idx}")
def get_img(idx:int,k:str):
    idx=idx-1
    return chain.return_img_str(idx,k)
@app.get("/files")
def get_files():
    return len(chain.chain)
'''
'''
def create_thumbnail(file:str):
    with open(file,"rb") as f:
        binary=f.read()
    base64_string = base64.b64encode(binary)
    return base64_string

@app.post("/register/uname")
def register(uname:str):
    user=User(uname)
    user.save()
    return {"token":user.chain_obj.chain_tocken}

@app.post("/login")
def login(log_info:log_info):
    info=dict(log_info)
    user = User(info["uname"], info["auth_token"])
    
    # Assuming the User class will raise an error if authentication fails
    uname = str(user.uname)
    
    # Create a thumbnail response as a base64-encoded string
    thumbnail = [thumb.decode("utf-8") if isinstance(thumb, bytes) else thumb for thumb in user.thumbnail]
    
    # Create the content for the JSON response
    content = {
        "uname": uname,
        "thumbnail": thumbnail
    }
    
    # Use JSONResponse to return a response with JSON data
    response = JSONResponse(content=content)
    
    # Set a cookie in the response, with the token or session information
    response.set_cookie(
        key="id",          # The cookie key name
        value=info["auth_token"],  # You can set a real session value here
        httponly=True,             # Makes the cookie HTTP-only
        max_age=86400,             # 1 day expiry
        samesite="Lax",            # Adjust the SameSite attribute (Lax/Strict/None) based on your need
        secure=True                # True if you're serving over HTTPS, False for local development
    )
    
    return response

@app.post("/uploadFile/")
async def create_upload_file(file: UploadFile,enc_tocken:str,uname:str,auth_token:str):
    user=User(uname,auth_token)
    extension=file.content_type.split("/")[-1]
    with open (f"./temp.{extension}","xb") as temp:
        temp.write(file.file.read())
        temp.close()
        user.chain_obj.create_chain(enc_tocken,[f"./temp.{extension}"])
        
    user.thumbnail.append(create_thumbnail(f"./temp.{extension}"))
    print(user.thumbnail)
    user.save()
    thumbnail = [thumb.decode("utf-8") if isinstance(thumb, bytes) else thumb for thumb in user.thumbnail]
    os.remove(f"./temp.{extension}")
    return (thumbnail[-1])
'''
'''
from fastapi import FastAPI, File, UploadFile, Depends, Cookie, HTTPException
from fastapi.responses import JSONResponse
from user_auth import User
import os
import base64

app = FastAPI()

@app.post("/uploadFile/")
async def create_upload_file(
    file: UploadFile,
    enc_tocken: str,  # Still sent explicitly from the frontend
    uname: str = Cookie(None),  # Read uname from the cookie
    auth_token: str = Cookie(None)  # Read auth_token from the cookie
):
    # Check if required cookies are present
    if not uname or not auth_token:
        raise HTTPException(status_code=401, detail="User authentication required.")

    # Authenticate the user with uname and auth_token from the cookie
    user = User(uname, auth_token)
    if not user.auth(auth_token):
        raise HTTPException(status_code=403, detail="Invalid authentication token.")

    # Determine file extension for saving
    extension = file.content_type.split("/")[-1]
    temp_file_path = f"./temp.{extension}"

    # Save uploaded file to a temporary path
    with open(temp_file_path, "wb") as temp:
        temp.write(file.file.read())

    # Encrypt and add the file to the user's blockchain
    user.chain_obj.create_chain(enc_tocken, [temp_file_path])

    # Generate and save the thumbnail
    user.thumbnail.append(create_thumbnail(temp_file_path))
    print("Updated thumbnails:", user.thumbnail)
    user.save()

    # Convert the most recent thumbnail to a base64 string
    last_thumbnail = user.thumbnail[-1]
    if isinstance(last_thumbnail, bytes):
        last_thumbnail = last_thumbnail.decode("utf-8")

    # Clean up the temporary file
    os.remove(temp_file_path)

    # Return the last thumbnail as the result
    return JSONResponse(content=last_thumbnail)
'''
'''
@app.get("/file/{idx}")
def get_img(idx:int,k:str,uname:str,auth_token:str):
    idx=idx-1
    user=User(uname,auth_token)
    return user.chain_obj.return_img_str(idx,k)
@app.get("/file")
def get_files(uname:str,auth_token:str):
    user=User(uname,auth_token)
    return({"number":user.no_of_files(),"thumbnails":user.thumbnail})
'''
from json import load
from fastapi import FastAPI, File, UploadFile, Depends, Cookie, HTTPException,Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Vault import block_chain
from user_auth import User
from pydantic import BaseModel, Field
import os
import base64
import pickle
from PIL import Image, ImageFilter



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function for creating thumbnails
def create_thumbnail(file_path: str,privacy:bool) -> str:
    img = Image.open(file_path)
    if privacy:
        blurred_img = img.filter(ImageFilter.BoxBlur(radius=60))
        blurred_img.save('./thumb.jpg')
    else:
        img.save('thumb.jpg')
    with open("./thumb.jpg", "rb") as f:
        binary_data = f.read()

    base64_string = base64.b64encode(binary_data).decode("utf-8")
    os.remove("./thumb.jpg")
    return base64_string

# Pydantic models
class LogInfo(BaseModel):
    uname: str = Field(..., description="Username of the user.")
    auth_token: str = Field(..., description="Authentication token for the user.")

class RegisterInfo(BaseModel):
    uname: str = Field(..., description="Username for registration.")

class FileUploadInfo(BaseModel):
    enc_tocken: str = Field(..., description="Encryption token for the file.")

class GetImageInfo(BaseModel):
    idx: int = Field(..., description="Index of the image to retrieve.")
    k: str = Field(..., description="Decryption key.")

class FileInfoResponse(BaseModel):
    number: int = Field(..., description="Total number of files for the user.")
    thumbnails: list[str] = Field(..., description="List of base64-encoded thumbnails.")

# Root route to check API status
@app.get("/")
def test():
    return "API is up and running."

# Register route
@app.post("/register/uname")
def register(info: RegisterInfo):
    user = User(info.uname)
    user.save()
    return {"token": user.chain_obj.chain_tocken}

# Login route
@app.post("/login")
def login(log_info: LogInfo):
    user = User(log_info.uname, log_info.auth_token)
    
    uname = user.uname
    thumbnails = [thumb.decode("utf-8") if isinstance(thumb, bytes) else thumb for thumb in user.thumbnail]

    response_content = {
        "uname": uname,
        "thumbnail": thumbnails
    }

    response = JSONResponse(content=response_content)
    response.set_cookie(
        key="auth_token",
        value=log_info.auth_token,
        httponly=True,
        max_age=86400,
        samesite="Lax",
        secure=True
    )

    return response

# Upload file route
@app.post("/uploadFile/")
async def create_upload_file(
    file: UploadFile,
    enc_tocken: str = Form(...),     # Retrieve enc_tocken from form data
    uname: str = Form(...),           # Retrieve uname from form data
    auth_token: str = Form(...),  # Retrieve auth_token from cookie named "id"
    privacy: bool = Form(...) 
):
    # Ensure auth_token is present
    if not auth_token:
        raise HTTPException(status_code=401, detail="User authentication required.")
    
    # Authenticate the user
    user = User(uname, auth_token)
    if not user.auth(auth_token):
        raise HTTPException(status_code=403, detail="Invalid authentication token.")
    
    # Determine file extension and save it temporarily
    extension = file.content_type.split("/")[-1]
    temp_file_path = f"./temp.{extension}"

    with open(temp_file_path, "wb") as temp:
        temp.write(await file.read())

    # Encrypt the file and add it to the user's blockchain
    user.chain_obj.create_chain(enc_tocken, [temp_file_path])

    # Create and store the thumbnail
    user.thumbnail.append(create_thumbnail(temp_file_path,privacy))
    user.save()

    # Get the last thumbnail as a base64 string
    last_thumbnail = user.thumbnail[-1]
    last_thumbnail = last_thumbnail.decode("utf-8") if isinstance(last_thumbnail, bytes) else last_thumbnail

    # Clean up the temporary file
    os.remove(temp_file_path)

    return JSONResponse(content=last_thumbnail)
# Get image by index route
@app.get("/file/{idx}")
def get_img(idx: int, k: str, uname: str, auth_token: str):
    if not uname or not auth_token:
        raise HTTPException(status_code=401, detail="User authentication required.")
    
    user = User(uname, auth_token)
    if not user.auth(auth_token):
        raise HTTPException(status_code=403, detail="Invalid authentication token.")
    
    idx = idx - 1
    return user.chain_obj.return_img_str(idx, k)
@app.post("/delete/{idx}")
def delete_img(idx:int,k:str,uname:str,auth_token:str):
    if not uname or not auth_token:
        raise HTTPException(status_code=401, detail="User authentication required.")
    
    user = User(uname, auth_token)
    if not user.auth(auth_token):
        raise HTTPException(status_code=403, detail="Invalid authentication token.")
    
    idx = idx - 1
    user.del_thumbnail(idx)
    user.save()
    return user.chain_obj.delete_img(idx, k) 
# Get all files route
@app.get("/file", response_model=FileInfoResponse)
def get_files(uname: str = Cookie(None), auth_token: str = Cookie(None)):
    if not uname or not auth_token:
        raise HTTPException(status_code=401, detail="User authentication required.")
    
    user = User(uname, auth_token)
    if not user.auth(auth_token):
        raise HTTPException(status_code=403, detail="Invalid authentication token.")

    return {"number": user.no_of_files(), "thumbnails": user.thumbnail}


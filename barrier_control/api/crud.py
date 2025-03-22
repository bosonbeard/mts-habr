from fastapi import APIRouter, HTTPException,  Depends,  Body
from .config import *
from pydantic import BaseModel, Field
from typing import Optional, List, Annotated
import sqlite3
from .log import logger
from fastapi.security import APIKeyHeader

API_KEY = "12345"  # Replace with your key

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True, description="API Key required for access")

async def get_api_key(api_key_header: Annotated[str, Depends(api_key_header)]):
    """
    Dependency to validate the API key from the header.
    """
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")




class Message(BaseModel):
    message:str 

class User(BaseModel):
    id: int
    phone: int
    name: str
    last_name: str
    position: Optional[str] = None

class CreatedUser(BaseModel):
    phone: int = Field(...,  description="User's phone.")
    name: str = Field(...,  description="User's name.")
    last_name: str = Field(...,  description="User's last name.")
    last_name: str
    position: Optional[str] = Field(None, description="user position (optional).")

class CreatedBarrier(BaseModel):
    zone: int = Field(...,  description="Security zone (location of the barrier on the site plan).")
    phone: int = Field(...,  description="Phone of GSM module for opening barrier.")   


class Barrier(BaseModel):
    id: int
    zone: int 
    phone: int 

class Access(BaseModel):
    user_phone: int
    barrier_zone: int


def read_tables(table, id=None):
    """
    Function for read users and barriers from db.
    """
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    where = ""
    if id:
        where = f" WHERE `id` = {id}"
    cursor.execute(f'SELECT * FROM {table} {where}')
    column_names = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    response = [dict(zip(column_names, row)) for row in rows]
    connection.close()
    if not response:
        return None
    return response[0] if id else response

def update_tables(table, operation, data=None, id=None):
    """
    Function for read users, barriers, and accesses from DB.
    """
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()
        sql_data = ()
        fields = {
            "users":("phone", "name", "last_name", "position"),
            "barriers":("zone", "phone"),
            "users_access":("user_phone", "barrier_zone")
            }
        if data:
            match table:
                case "users":
                    sql_data = (data.phone, data.name, data.last_name, data.position)
                case "barriers":
                    sql_data = (data.zone, data.phone)
                case "users_access":
                    sql_data = (data.user_phone, data.barrier_zone)
        match operation:
            case "create":
                values=[]
                for field in fields[table]:
                     values.append(f'?')
                result_string = ', '.join(values)
                sql = f'UPDATE {table} SET {result_string} Where id = {id}'
                sql = f'INSERT INTO {table} {fields[table]} VALUES ({result_string})'
                cursor.execute(sql, sql_data)
                connection.commit()
            case "delete":
                sql =""
                if id:
                    sql = f'DELETE FROM {table}  WHERE id = {id}'
                elif data:
                    sql = f'DELETE FROM {table}  WHERE user_phone = {data.user_phone} AND barrier_zone = {data.barrier_zone} '
                cursor.execute(sql)
                connection.commit()
            case "update":
                update_fields = []
                for field in fields[table]:
                     update_fields.append(f'{field} = ?')
                result_string = ', '.join(update_fields)
                sql = f'UPDATE {table} SET {result_string} Where id = {id}'
                sql_data = tuple(data.model_dump().values())
                cursor.execute(sql, sql_data)
                connection.commit()
            case None:
                return None
    except sqlite3.Error as e:
            print(f"Error: {e}")
            return None
    finally:
            if connection:
                connection.close()
    return cursor.lastrowid




router = APIRouter(tags=["CRUD"])


@router.get("/bariers/", response_model=List[Barrier])
async def list_bariers(api_key: Annotated[str, Depends(get_api_key)]):
    """
    List all barriers.
    """
    response = read_tables(BARIERS_TABLE)
    return response

@router.get("/barrier/{barrier_id}", response_model=Barrier)
async def list_barrier(barrier_id: int, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Get a barrier with specific id.
    """
    response = read_tables(BARIERS_TABLE, barrier_id)
    if not response:
        raise HTTPException(status_code=404, detail="Barrier not found")
    return response


@router.post("/barriers/", response_model=Message)
async def create_barrier(barrier: CreatedBarrier, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Creates a new barrier.
    """
    result = update_tables(BARIERS_TABLE, "create", data=barrier)
    if result == None:
         raise HTTPException(status_code=400, detail="Bad request")
    logger.info(f'barrier created {barrier}')
    return {"message": f"created barrier with id = {result}"}

@router.delete("/barriers/{barrier_id}", response_model=Message)
async def delete_barrier(barrier_id:int, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Delete a barrier with specific id.
    """
    result = update_tables(BARIERS_TABLE, "delete", None, barrier_id)
    if result == None:
         raise HTTPException(status_code=400, detail="Bad request")
    logger.info(f'barrier {barrier_id} deleted')
    return {"message":"ok"}


@router.patch("/barriers/{barrier_id}", response_model=Message)
async def edit_barrier(barrier_id:int, barrier:CreatedBarrier,api_key: Annotated[str, Depends(get_api_key)]):
    """
    Update a barrier with specific id (fill in all the request attributes).
    """
    result = update_tables(BARIERS_TABLE, "update", barrier, barrier_id)
    if result == None:
         raise HTTPException(status_code=400, detail="Bad request")
    logger.info(f'barrier {barrier_id} updated {barrier}')
    return {"message":"ok"}

@router.get("/accesses/", response_model=List[Access])
async def list_accesses(api_key: Annotated[str, Depends(get_api_key)]):
    """
    List accesses (user to barrier).
    """
    response = read_tables(ACCESS_TABLE)
    return response

@router.post("/accesses/", response_model=Message)
async def create_access(access: Access, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Creates a new access (user to barrier).
    """
    result = update_tables(ACCESS_TABLE, "create", data=access)
    if result == None:
         raise HTTPException(status_code=400, detail="Bad request")
    logger.info(f'user access created {access}')
    return {"message": f"created access with id = {result}"}

@router.delete("/accesses/", response_model=Message)
async def delete_user(access:Access, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Delete access (user to barrier).
    """
    result = update_tables(ACCESS_TABLE, "delete",access, None)
    if result == None:
         raise HTTPException(status_code=400, detail="Bad request")
    logger.info(f'user access deleted {access}')
    return {"message":"ok"}



@router.get("/users/", response_model=List[User])
async def list_users(api_key: Annotated[str, Depends(get_api_key)]):
    """
    List all users.
    """
    response = read_tables(USER_TABLE)
    return response


@router.get("/users/{user_id}", response_model=User)
async def list_user(user_id: int, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Get a user with specific id.
    """
    response = read_tables(USER_TABLE, user_id)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response

@router.post("/users/", response_model=Message)
async def create_user(user: CreatedUser, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Creates a new user.
    """
    result = update_tables(USER_TABLE, "create", data=user)
    if result == None:
         raise HTTPException(status_code=400, detail="Bad request")
    logger.info(f'user created {user}')
    return {"message": f"created  user with id {result}"}

@router.delete("/users/{user_id}", response_model=Message)
async def delete_user(user_id:int, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Delete a user with specific id.
    """
    result = update_tables(USER_TABLE, "delete", None, user_id)
    if result == None:
         raise HTTPException(status_code=400, detail="Bad request")
    logger.info(f'user_id = {user_id} deleted')
    return {"message":"ok"}


@router.patch("/users/{user_id}", response_model=Message)
async def edit_user(user_id:int, user:CreatedUser, api_key: Annotated[str, Depends(get_api_key)]):
    """
    Update a user
      with specific id (fill in all the request attributes).
    """
    result = update_tables(USER_TABLE, "update", user, user_id)
    if result == None:
         raise HTTPException(status_code=400, detail="Bad request")
    logger.info(f'user_id = {user_id} updated {user}')
    return {"message":"ok"}

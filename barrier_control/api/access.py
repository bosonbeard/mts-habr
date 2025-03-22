from fastapi import APIRouter, HTTPException,  Body
from pydantic import BaseModel
from typing import  List,  Union, Any
import sqlite3

from .config import * 
from .log import logger


EVENT_URL = "<url or IP>/logs"
CLIENT_ID = "MTC Exolve client ID"
DISPLAY_NUMBER  = "MTC Exolve phone number"


class FollowMeRule(BaseModel):
    I_FOLLOW_ORDER: str
    ACTIVE: str
    NAME: str
    REDIRECT_NUMBER: str
    PERIOD: str
    PERIOD_DESCRIPTION: str
    TIMEOUT: str

class FollowMeStruct(BaseModel):
    List[FollowMeRule]  

class Result(BaseModel):
    redirect_type: int
    event_URL: str
    client_id: str
    event_extended: str
    masking: str
    display_number: str
    followme_struct: List[Union[int, List[FollowMeRule]]]  

class ExolveResponse(BaseModel):
    id: int
    jsonrpc: str
    result: Result


def open_barriers(phone):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(f'''SELECT phone from {BARIERS_TABLE} as b 
    JOIN {ACCESS_TABLE} as u on b.zone = u.barrier_zone 
    where u.user_phone = {phone} ''')
    column_names = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    response = [dict(zip(column_names, row)) for row in rows]
    connection.close()
    return response


router = APIRouter(tags=["Access control"])


@router.post("/access/", response_model=ExolveResponse)
async def response_to_exolve(body: Any = Body(None)):
    """
    Get response to MTC Exolve for redirect phone call to barrier GSM \n (s.a [documentation](https://wiki.exolve.ru/pages/viewpage.action?pageId=106332539))
    """

    if 'params' in body and 'numberA' in body['params']:
        user_phone = body["params"]["numberA"]
    else:
        raise HTTPException(status_code=400, detail="Bad request.Filed params.numberA required")
    barrier_phones =  open_barriers(user_phone)
    if (barrier_phones == None):
        raise HTTPException(status_code=403, detail="Access to barriers not allowed")
    followme_struct = []
    for i in range(0, len(barrier_phones) ) :
        row = barrier_phones[i]
        followme_struct.append(            {
                "I_FOLLOW_ORDER": str(i+1),
                "ACTIVE": "Y",
                "NAME": "BARRIER_PHONE",
                "REDIRECT_NUMBER": str(row["phone"]),
                "PERIOD": "always",
                "PERIOD_DESCRIPTION": "always",
                "TIMEOUT": "30"
            })
        # Создаем объект Result
    result_object = Result(

        redirect_type="3",
        event_URL=EVENT_URL ,
        client_id= CLIENT_ID,
        event_extended="N",
        masking= "Y",
        display_number= DISPLAY_NUMBER,
        followme_struct=[len(followme_struct),followme_struct] 
    ) 
    exolve_response_object = ExolveResponse(
            id=1,
            jsonrpc="2.0",
            result=result_object
    )
    logger.info(f'barriers {barrier_phones} try to open for {user_phone}')
    return exolve_response_object
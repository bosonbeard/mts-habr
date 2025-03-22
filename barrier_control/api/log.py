
from fastapi import APIRouter, Body
from typing import Any
from . import config 
import logging.config


router = APIRouter(tags=["Logs"])

logging.config.dictConfig(config.LOGGING)
logger = logging.getLogger('myapp')

@router.post('/logs')
async def get_body(body: Any = Body(None)):
    """
    Create log for MTC Exolve events.
    """
    logger.info(f'log endpoint was called. body: {body}')
    return body
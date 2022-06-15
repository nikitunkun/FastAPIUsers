from typing import Dict

from pydantic import BaseModel


class ResponseBase(BaseModel):
    data: Dict

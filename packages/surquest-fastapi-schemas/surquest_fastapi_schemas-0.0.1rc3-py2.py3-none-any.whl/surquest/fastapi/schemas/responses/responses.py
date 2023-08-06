from pydantic import BaseModel
from .info import InfoSuccess, InfoWarning, InfoError
from .metadata import Metadata
from typing import Union, List, Dict, Optional


class ResponseSuccess(BaseModel):
    info: InfoSuccess = InfoSuccess()
    meta: Optional[Metadata] = None
    data: Union[List, Dict]


class ResponseWarning(BaseModel):

    info: InfoWarning = InfoWarning()
    meta: Optional[Metadata] = None
    data: Optional[Union[List, Dict]] = None

    @classmethod
    def set(cls, warnings, data):

        return cls(
            info=InfoWarning(warnings=warnings),
            data=data
        )


class ResponseError(BaseModel):
    info: InfoError = InfoError()

    @classmethod
    def set(cls, errors, warnings=[]):
        return cls(
            info=InfoError(
                warnings=warnings,
                errors=errors
            )
        )

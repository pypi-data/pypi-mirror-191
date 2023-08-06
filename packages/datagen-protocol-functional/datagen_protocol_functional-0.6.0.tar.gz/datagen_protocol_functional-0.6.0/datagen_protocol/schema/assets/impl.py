from enum import Enum
from typing import Union, List, TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel
from pydantic.fields import ModelField, Field


A = TypeVar("A")


class AttributesList(list, Generic[A]):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[A, List[A]], field: ModelField) -> List[A]:
        if not isinstance(v, list):
            v = [v]
        return [field.type_(v_) for v_ in v]


AA = TypeVar("AA")

AP = TypeVar("AP")


class AssetAttributes(BaseModel):
    class Config:
        frozen = True


class Asset(GenericModel, Generic[AA]):
    attributes: AA = Field(default=None)

    def dict(self, *args, **kwargs):
        kwargs["exclude"] = {"attributes"}
        return super().dict(*args, **kwargs)


class PresetAsset(GenericModel, Generic[AA, AP]):
    attributes: AA = Field(default=None)
    presets: AP = Field(default=None)

    def dict(self, *args, **kwargs):
        kwargs["exclude"] = {"attributes", "presets"}
        return super().dict(*args, **kwargs)

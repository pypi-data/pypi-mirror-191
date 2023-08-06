from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from datagen_protocol.config import conf
from datagen_protocol.schema import fields, ExtrinsicParams
from datagen_protocol.schema.assets.impl import Asset, AssetAttributes, PresetAsset
from datagen_protocol.schema.assets.attributes import (
    HICDomain,
    HICSubDomain,
    HumanBehaviour,
    Ethnicity,
    Age,
    Gender,
)
from datagen_protocol.schema.environment import Background, Camera, Light


class SequenceAttributes(AssetAttributes):
    domain: HICDomain
    sub_domain: HICSubDomain
    behaviour: HumanBehaviour
    ethnicity: Ethnicity
    gender: Gender
    age: Age


class SequencePresets(BaseModel):
    cameras: Dict[str, ExtrinsicParams]
    clutter_areas: List[str]


class ClutterLevel(str, Enum):
    NONE = "none"  # 0
    LOW = "low"  # 8
    MEDIUM = "medium"  # 16
    HIGH = "high"  # 32


class DataSequence(PresetAsset[SequenceAttributes, SequencePresets]):
    id: str
    camera: Camera = Field(default_factory=Camera)
    background: Optional[Background] = None
    lights: Optional[List[Light]] = Field(default_factory=list)
    clutter_areas: Dict[str, ClutterLevel] = Field(default_factory=dict)

from enum import Enum
from typing import Optional, List

from pydantic import Field, BaseModel

from datagen_protocol.schema.assets.attributes import (
    Age,
    Ethnicity,
    Gender,
    HairLength,
    FacialHairStyle,
    HairStyle,
    EyesColor,
)
from datagen_protocol.schema.assets.impl import Asset, AttributesList, AssetAttributes
from datagen_protocol.config import conf
from datagen_protocol.schema import fields
from datagen_protocol.schema.d3 import Point, Vector, Rotation
from datagen_protocol.schema.humans.accessories import Accessories
from datagen_protocol.schema.environment import Camera, Background, Light


class HairColor(BaseModel):
    melanin: float = fields.numeric(conf.human.hair.melanin)
    redness: float = fields.numeric(conf.human.hair.redness)
    whiteness: float = fields.numeric(conf.human.hair.whiteness)
    roughness: float = fields.numeric(conf.human.hair.roughness)
    index_of_refraction: float = fields.numeric(conf.human.hair.refraction)


class HairModel(BaseModel):
    id: str
    color_settings: HairColor = Field(default_factory=HairColor)


class HairAttributes(AssetAttributes):
    age_group_match: AttributesList[Age]
    ethnicity_match: AttributesList[Ethnicity]
    gender_match: AttributesList[Gender]
    length: HairLength
    style: AttributesList[HairStyle]


class FacialHairAttributes(AssetAttributes):
    style: FacialHairStyle


class EyebrowsAttributes(AssetAttributes):
    age_group_match: AttributesList[Age]
    ethnicity_match: AttributesList[Ethnicity]
    gender_match: AttributesList[Gender]


class Hair(HairModel, Asset[HairAttributes]):
    pass


class FacialHair(HairModel, Asset[FacialHairAttributes]):
    pass


class Eyebrows(HairModel, Asset[EyebrowsAttributes]):
    pass


class Gaze(BaseModel):
    distance: float = fields.numeric(conf.human.eyes.gaze.distance)
    direction: Vector = fields.vector(conf.human.eyes.gaze.direction)


class EyesAttributes(AssetAttributes):
    color: EyesColor


class Eyes(Asset[EyesAttributes]):
    id: str
    target_of_gaze: Gaze = Field(default_factory=Gaze)
    eyelid_closure: float = fields.numeric(conf.human.eyes.eyelid_closure)


class ExpressionName(str, Enum):
    NEUTRAL = "none"
    HAPPINESS = "happiness"
    SADNESS = "sadness"
    SURPRISE = "surprise"
    FEAR = "fear"
    ANGER = "anger"
    DISGUST = "disgust"
    CONTEMPT = "contempt"
    MOUTH_OPEN = "mouth_open"


class Expression(BaseModel):
    name: ExpressionName = fields.enum(ExpressionName, conf.human.expression.name)
    intensity: float = fields.numeric(conf.human.expression.intensity)


class Head(BaseModel):
    eyes: Eyes
    hair: Optional[Hair]
    eyebrows: Optional[Eyebrows]
    facial_hair: Optional[FacialHair]
    expression: Expression = Field(default_factory=Expression)
    location: Point = fields.point(conf.human.head.location)
    rotation: Rotation = fields.rotation(conf.human.head.rotation)


class HumanAttributes(AssetAttributes):
    ethnicity: Ethnicity
    age: Age
    gender: Gender


class Human(Asset[HumanAttributes]):
    id: str
    head: Head


class HumanDatapoint(BaseModel):
    human: Human
    camera: Camera
    accessories: Optional[Accessories]
    background: Optional[Background]
    lights: Optional[List[Light]]

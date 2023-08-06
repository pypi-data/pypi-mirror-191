from typing import Optional

from pydantic import BaseModel, Field

from datagen_protocol.config import conf
from datagen_protocol.schema import fields
from datagen_protocol.schema.assets.impl import AssetAttributes, Asset
from datagen_protocol.schema.assets.attributes import Environment, TimeOfDay, Generator


class BackgroundAttributes(AssetAttributes):
    environment: Environment
    time_of_day: TimeOfDay
    generator: Generator


class Background(Asset[BackgroundAttributes]):
    id: str
    rotation: float = fields.numeric(conf.background.rotation)
    transparent: bool = fields.bool(conf.background.transparency)

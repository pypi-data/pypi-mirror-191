from typing import List, Union

from pydantic import BaseModel

from datagen_protocol import __version__ as __datagen_protocol_version__
from datagen_protocol.schema.hic.sequence import DataSequence
from datagen_protocol.schema.humans import HumanDatapoint


class DataRequest(BaseModel):
    __protocol_version__: str = __datagen_protocol_version__

    datapoints: List[Union[DataSequence, HumanDatapoint]]

    def __len__(self):
        return len(self.datapoints)

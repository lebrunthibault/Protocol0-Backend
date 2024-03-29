from typing import List, Dict, Union, Optional

from protocol0.domain.lom.device.DeviceEnum import DeviceEnum
from protocol0.domain.lom.device.DeviceEnumGroup import DeviceEnumGroup
from protocol0.domain.lom.sample.SampleCategoryEnum import SampleCategoryEnum
from pydantic import BaseModel

from lib.ableton_set import AbletonSet, AbletonSetManager


class ServerState(BaseModel):
    set: Optional[AbletonSet]
    set_shortcuts: List[str]
    sample_categories: Dict[str, List[str]]
    favorite_device_names: List[List[Union[str, Dict]]]

    @classmethod
    def create(cls) -> "ServerState":
        def serialize_device_enum(d: Union[DeviceEnum, DeviceEnumGroup]) -> Union[str, Dict]:
            if isinstance(d, DeviceEnum):
                return d.name
            else:
                return d.to_dict()

        return ServerState(
            set=AbletonSetManager.active().dict() if AbletonSetManager.has_active_set() else None,
            set_shortcuts=["last", "default", "new"],
            sample_categories={
                category.name.lower(): category.subcategories
                for category in list(SampleCategoryEnum)
            },
            favorite_device_names=[
                list(map(serialize_device_enum, row)) for row in DeviceEnum.favorites()
            ],
        )

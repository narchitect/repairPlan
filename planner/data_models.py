from dataclasses import dataclass, field
from typing import List, Dict, Any
from pydantic import BaseModel
from typing import Union

@dataclass
class Door(BaseModel):
    door_id: int

@dataclass
class Room(BaseModel):
    room_id: int
@dataclass
class ScanningInfo(BaseModel):
    position: Dict[str, float]
    direction: Dict[str, float]
@dataclass
class TaskData(BaseModel):
    user_description: str
    defect_id: int
    robot_id: int
    room_id: int
    navigation_path: List[Union[Door, Room]]
    scanning_info: ScanningInfo
    robotTasks: List[str]

from dataclasses import dataclass, field
from typing import List, Dict, Any
from pydantic import BaseModel
from typing import Union



class ScanningInfo(BaseModel):
    position: List[float]
    direction: List[float]

class Reason(BaseModel):
    int_reason: str
    nav_reason: str
    scan_reason: str
    act_reason: str

class TaskData(BaseModel):
    user_description: str
    defect_id: int
    robot_id: int
    room_id: str
    navigation_path: List[int]
    scanning_info: ScanningInfo
    robotTasks: List[str]
    reasons: Reason

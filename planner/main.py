from data.robots import robots_withConfig
from utils.loader import load_scene_graph, get_node_info, get_rooms_info, get_robot_info_by_id
from planner.planner_initialPlanner import get_initialPlan
from planner.planner_navigation_SDK2 import get_navigationPath
from planner.data_models import TaskData, ScanningInfo, Reason
from planner.planner_scanning_SDK import get_scanning_plan
from planner.planner_repair_SDK import get_repair_plan
import asyncio

def main():

    #prepare inputs
    user_description = "there is a crak on the wall with window in the room id 1"
    scene_graph = load_scene_graph("../data/sceneGraphs/3dsg_withCOR_int.json")
    robot_DB = robots_withConfig

    #initial Plan
    defect_id, robot_id, int_reasoning = get_initialPlan(user_description, robot_DB, scene_graph)
    print(defect_id, robot_id, int_reasoning)
    print(type(int_reasoning))

    #Navigation Plan
    defect_info = get_node_info(defect_id, scene_graph)
    path, nav_reasoning = get_navigationPath(defect_info,scene_graph, robot_DB)
    print(path, nav_reasoning)

    #Scanning Plan
    room_info = get_rooms_info(defect_id, scene_graph)
    camera_FOV = 90
    position, direction, scan_reasoning = get_scanning_plan(room_info, camera_FOV)
    print(position, direction, scan_reasoning)

    #Repair Plan
    room_info = get_rooms_info(342, scene_graph)
    selected_robot = get_robot_info_by_id(robot_id)
    actions, act_reasoning = get_repair_plan(user_description, selected_robot, room_info)
    print(actions, act_reasoning)

    #final plan
    scanning_info = ScanningInfo(
        position=position,
        direction=direction,
    )
    reasons = Reason(
        int_reason=int_reasoning,
        nav_reason=nav_reasoning,
        scan_reason=scan_reasoning,
        act_reason=act_reasoning
    )
    final_plan = TaskData(
        user_description=user_description,
        defect_id=defect_id,
        robot_id=robot_id,
        room_info=room_info,
        navigation_path=path,
        scanning_info=scanning_info,
        robotTasks=actions,
        reasons=reasons
    )

    print(final_plan)

if __name__ == "__main__":
    main()

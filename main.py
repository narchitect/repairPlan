from data.robots import robots_withConfig
from utils.loader import load_scene_graph, get_robot_info_by_id
from planner.planner_initialPlanner import get_initialPlan
from planner.planner_navigation_SDK2 import get_navigationPath
from planner.data_models import TaskData, ScanningInfo, Reason
from planner.planner_scanning_SDK import get_scanning_plan
from planner.planner_repair_SDK import get_repair_plan
from visualizer.vis_navigation import visualize_navigation
from visualizer.vis_scanning import visualize_scanning  

def main():
    #prepare inputs
    user_description = "there is a crak on the wall with window in the room id 1"
    scene_graph = load_scene_graph("/Users/nayunkim/Documents/GitHub/repairPlan/data/sceneGraphs/3dsg_withCOR_int.json")
    robot_DB = robots_withConfig

    #initial Plan
    defect_id, robot_id, room_id, int_reasoning = get_initialPlan(user_description, robot_DB, scene_graph)
    print("initial planning finished")

    #Navigation Plan
    path, nav_reasoning = get_navigationPath(defect_id, scene_graph, robot_DB)
    print("navigation planning finished")
    
    #Scanning Plan
    position, direction, scan_reasoning = get_scanning_plan(defect_id, robot_id)
    print("scanning planning finished")

    #Repair Plan
    actions, act_reasoning = get_repair_plan(user_description, defect_id, robot_id)
    print("repair planning finished")

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
        room_id=room_id,
        navigation_path=path,
        scanning_info=scanning_info,
        robotTasks=actions,
        reasons=reasons
    )

    print(final_plan)

    camera_fov = get_robot_info_by_id(robot_id)["robots"]["camera"]["FOV"]

    visualize_navigation(path, scene_graph, "./data/image/top_view.png", "./data/image/nav_test1.png")
    visualize_scanning(defect_id, camera_fov, position, direction)

if __name__ == "__main__":
    main()

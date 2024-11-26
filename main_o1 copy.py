from data.robots2 import robots_withConfig
from utils.loader import load_scene_graph, get_robot_info_by_id
from planner.planner_initialPlanner_o1 import identify_defect_node, select_robot
from planner.planner_navigation_o1 import get_navigationPath_o1
from planner.planner_repair import get_repair_plan
from planner.planner_scanning_o1 import get_scanning_plan_o1
from planner.data_models import TaskData, ScanningInfo, Reason
from visualizer.vis_navigation import visualize_navigation
from visualizer.vis_scanning_withComp import visualize_scanning  

def main():
    #prepare inputs
    user_description = "there is a crak on the wall in the room 13"
    scene_graph = load_scene_graph("/Users/nayunkim/Documents/GitHub/repairPlan/data/sceneGraphs/new_structure/3dsg_full.json")
    robot_DB = robots_withConfig

    #initial Plan
    defect_id, room_id = identify_defect_node(user_description, scene_graph)
    robot_id = select_robot(user_description,defect_id, robot_DB)
    print(f"initial planning finished. defect_id: {defect_id}, room_id: {room_id}, robot_id: {robot_id}")

    #Navigation Plan
    path = get_navigationPath_o1(room_id, scene_graph)
    print(f"navigation planning finished. path: {path}")
    
    #Scanning Plan
    optimal_position, optimal_direction = get_scanning_plan_o1(defect_id, robot_id)
    print(f"scanning planning finished. optimal_position: {optimal_position}, optimal_direction: {optimal_direction}")

    #Repair Plan
    actions, act_reasoning = get_repair_plan(user_description, defect_id, robot_id)
    print(f"repair planning finished. actions: {actions}, act_reasoning: {act_reasoning}")

    #final plan
    scanning_info = ScanningInfo(
        position=optimal_position,
        direction=optimal_direction,
    )

    final_plan = TaskData(
        user_description=user_description,
        defect_id=defect_id,
        robot_id=robot_id,
        room_id=room_id,
        navigation_path=path,
        scanning_info=scanning_info,
        robotTasks=actions,
    )

    print(final_plan)

    visualize_navigation(path, scene_graph, "./data/image/top_view.png", "./data/image/nav_test1.png")
    visualize_scanning(defect_id, robot_id, optimal_position, optimal_direction)

if __name__ == "__main__":
    main()

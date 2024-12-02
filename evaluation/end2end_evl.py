from data.robots2 import robots_withConfig
from planner.planner_initialPlanner_o1_wo_question import identify_defect_node, select_robot
from planner.planner_navigation_o1 import get_navigationPath_o1
from planner.planner_repair_o1 import get_repair_plan
from planner.planner_scanning_o1 import get_scanning_plan_o1
from planner.data_models import TaskData, ScanningInfo, Reason
from visualizer.vis_navigation import visualize_navigation
from visualizer.vis_scanning_withComp import visualize_scanning  

def evaluate_end2end(user_description, scene_graph, robot_DB, gpt_model):
    defect_id, room_id = identify_defect_node(user_description, scene_graph, gpt_model)
    robot_id = select_robot(user_description, defect_id, robot_DB, gpt_model)
    print(f"initial planning finished. defect_id: {defect_id}, room_id: {room_id}, robot_id: {robot_id}")

    try:
        path = get_navigationPath_o1(room_id, scene_graph, gpt_model)
        print(f"navigation planning finished. path: {path}")
    except Exception as e:
        print(f"Error in navigation planning: {e}")
        path = None

    try:
        optimal_position, optimal_direction = get_scanning_plan_o1(defect_id, robot_id, gpt_model)
        print(f"scanning planning finished. optimal_position: {optimal_position}, optimal_direction: {optimal_direction}")
    except Exception as e:
        print(f"Error in scanning planning: {e}")
        optimal_position, optimal_direction = None, None

    try:
        actions = get_repair_plan(user_description, defect_id, robot_id, gpt_model)
        print(f"repair planning finished. actions: {actions}")
    except Exception as e:
        print(f"Error in repair planning: {e}")
        actions = None

    if path:
        input_image_path = "/Users/nayunkim/Documents/GitHub/repairPlan/data/images/top_view.png"
        output_image_path = f"/Users/nayunkim/Documents/GitHub/repairPlan/outputs/end2end_evl/{user_description}_{gpt_model}.png"
        visualize_navigation(path, defect_id, scene_graph, input_image_path, output_image_path)
    if optimal_position and optimal_direction:
        visualize_scanning(defect_id, robot_id, optimal_position, optimal_direction)



from planner.planner_navigation import get_inspectionPlan
from planner.planner_scanning import find_optimal_location
from planner.planner_repair import plan_robot_task
from utils.get_room_nodes import get_associated_nodes
from visualizer.vis_scanning import visualize_scanPosition
from visualizer.vis_navigation import overlay_navigation_path
from data.robots import get_robot_info_by_id
def get_repair_plan (user_description, scene_graph, robot_library, robot_location, camera_fov):
    final_plan = []

    #step1: inspection plan
    inspection_plan_json = get_inspectionPlan(user_description, scene_graph, robot_library, robot_location)
    print(inspection_plan_json)
    final_plan.append(inspection_plan_json)

    #visualization navigation paths
    overlay_image_path = '../data/image/top_view.png'
    output_image_path = '../data/output/navigation_path.png'
    navigation_path = inspection_plan_json['navigation_path']
    print (navigation_path)
    # overlay_navigation_path(navigation_path, scene_graph,  overlay_image_path, output_image_path)

    #step2: optimal position
    env_info = get_associated_nodes(inspection_plan_json['defect_node'])

    optimal_camera_json = find_optimal_location(env_info, camera_fov)
    print(optimal_camera_json)
    final_plan.append(optimal_camera_json)

    #visualization scanning position
    camera_location = optimal_camera_json['optimal_location']
    camera_direction = optimal_camera_json['optimal_direction']
    visualize_scanPosition(env_info, camera_fov, camera_location, camera_direction)

    #step3: repair action sequence
    re_acc_robots = get_robot_info_by_id(inspection_plan_json['reachable_accessible_robots'])
    repair_plan_json =plan_robot_task(user_description, re_acc_robots, env_info)
    print(repair_plan_json)
    final_plan.append(repair_plan_json)

    return final_plan






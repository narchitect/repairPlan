from data.robots import robots_withConfig
from utils.loader import load_scene_graph, get_node_by_id
from planner.planner_initialPlanner import get_initialPlan
from planner.planner_navigation_SDK2 import get_navigationPath
from planner.data_models import TaskData
def main():

    #prepare inputs
    user_description = "there is a crak on the wall with window in the room id 1"
    scene_graph = load_scene_graph("../data/sceneGraphs/3dsg_withCOR_int.json")
    robot_DB = robots_withConfig

    #initial Plan
    defect_id, robot_id, int_reasoning = get_initialPlan(user_description, robot_DB, scene_graph)
    print(defect_id, robot_id, int_reasoning)

    #Navigation Plan
    defect_info = get_node_by_id(defect_id, scene_graph)
    path, nav_reasoning = get_navigationPath(defect_info,scene_graph, robot_DB)
    print(path, nav_reasoning)

    #

if __name__ == "__main__":
    main()
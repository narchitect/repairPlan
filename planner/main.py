from data.robots import robots
from utils.loader import load_scene_graph
from planner.planner_initialPlanner import get_initialPlan
from planner.data_models import TaskData
def main():

    user_description = "there is a crak on the wall with window in the room id 1"
    scene_graph = load_scene_graph("../data/sceneGraphs/3dsg_withIds.json")
    defect_id, robot_id, reasoning = get_initialPlan(user_description, robots, scene_graph)

    print(defect_id, robot_id, reasoning)

if __name__ == "__main__":
    main()
from planner.planner_initialPlanner_o1_wo_question import identify_defect_node
from utils.loader import GLOBAL_SCENE_GRAPH
from typing import List, Tuple, Optional

scene_graph = GLOBAL_SCENE_GRAPH

# Define the test cases for simple and complex inputs along with their ground truths
simple_tests: List[Tuple[str, Tuple[Optional[int], Optional[int]]]] = [
    # (user_input, (Defect_id, Room_id))
    ("The wall with ID 1116 has a crack.", (1116, 7)),
    ("The wall with window ID 4055 needs to be painted.", (1042, 32)),
    ("The ceiling in room ID 32 is damaged.", (2055, 32)),
    ("The object located at [-26.1239, -7.47, 1.85] has a crack.", (1116, 7)),
    ("The ceiling with the size [9.799, 23.86, 0.0] has a crack.", (2024, 40)),
    ("The wall that has a window has a crack in room 11.", (1043, 11)),
    ("The wall with 8 doors in the room id 6 needs to be painted.", (1211, 6)),
    ("The wall that doesn't have any windows or doors in the rooom id 12 has a crack.", (1077, 12)),
    ("The wall with two windows in the room located at [-5.15925, -33.5286, 7.85] needs repainting.", (1036, 50)),
    ("The doors in room id 8 need to be cleaned.", ([5001, 5049], 8)),
]

complex_tests: List[Tuple[str, Tuple[Optional[int], Optional[int]]]] = [
    # (user_input, (Defect_id, Room_id))
    ("The largest door in the room id 9  is damaged.", (5000, 9)),
    ("The wall in room ID 18 closest to the boundary with room ID 19 has a crack.", (1093, 18)),
    ("The door in room ID 42 that connects to room ID 41 needs cleaning.", (5061, 42)),
    ("The wall located on the north side in room ID 40 has mold.", (1157, 40)),
    ("The wall to the immediate left after entering through door ID 5059 in room ID 39 has graffiti.", (1118, 39)),
    ("There seems to be water dripping from above in room ID 7, which may indicate a crack.", (2000, 7)),
    ("It feels like cold air is coming from outside in the room id 42.", (4022, 42)),
    ("The most northern door in the largest room is jammed.", (5065, 40)),
    ("The wall with one window in the room directly to the right of the entrance to room ID 26 has a crack.", (1024, 27)),
    ("Among the rooms with at least one door and one window, the window in the smallest room needs to be cleaned.", (4029, 54)),
]

def evaluate_identify_defect_node(gpt_model: str = "gpt-4o", simple_trial_ids: Optional[List[int]] = None, complex_trial_ids: Optional[List[int]] = None):
    simple_correct = 0
    complex_correct = 0

    print(f"=== Evaluation using model {gpt_model} ===\n")

    print("Evaluating Simple Inputs:\n")
    for idx, (user_input, ground_truth) in enumerate(simple_tests):
        if simple_trial_ids is not None and idx + 1 not in simple_trial_ids:
            continue

        predicted_defect_id, predicted_room_id = identify_defect_node(user_input, scene_graph, gpt_model)
        is_correct = (predicted_defect_id == ground_truth[0]) and (predicted_room_id == ground_truth[1])

        print(f"Test {idx + 1}: {user_input}")
        print(f"Predicted Defect ID: {predicted_defect_id}, Predicted Room ID: {predicted_room_id}")
        print(f"Ground Truth Defect ID: {ground_truth[0]}, Ground Truth Room ID: {ground_truth[1]}")
        print(f"Result: {'Correct' if is_correct else 'Incorrect'}\n")

        if is_correct:
            simple_correct += 1

    simple_accuracy = simple_correct / len(simple_tests) * 100
    print(f"Simple Inputs Accuracy: {simple_accuracy:.2f}%\n")

    print("Evaluating Complex Inputs:\n")
    for idx, (user_input, ground_truth) in enumerate(complex_tests):
        if complex_trial_ids is not None and idx + 1 not in complex_trial_ids:
            continue

        predicted_defect_id, predicted_room_id = identify_defect_node(user_input, scene_graph, gpt_model)
        is_correct = (predicted_defect_id == ground_truth[0]) and (predicted_room_id == ground_truth[1])

        print(f"Test {idx + 1}: {user_input}")
        print(f"Predicted Defect ID: {predicted_defect_id}, Predicted Room ID: {predicted_room_id}")
        print(f"Ground Truth Defect ID: {ground_truth[0]}, Ground Truth Room ID: {ground_truth[1]}")
        print(f"Result: {'Correct' if is_correct else 'Incorrect'}\n")

        if is_correct:
            complex_correct += 1

    complex_accuracy = complex_correct / len(complex_tests) * 100
    print(f"Complex Inputs Accuracy: {complex_accuracy:.2f}%\n")

    print(f"=== End of Evaluation Trial ===")
# Example usage:
# evaluate_identify_defect_node( gpt_model="gpt-4o")
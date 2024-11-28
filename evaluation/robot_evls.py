from planner.planner_initialPlanner_o1_wo_question import select_robot
from planner.planner_repair_o1 import get_repair_plan
from data.robots2 import robots_withConfig
from typing import List, Tuple

# Define the test cases for each category
direct_requests: List[Tuple[str, int, int, List[str]]] = [
    # (user_input, defect_id, ground_truth_robot_id, ground_truth_actions)
    (
        "The floor needs to be wiped with cleaning solution",
        3047,
        1,
        [
            'loadArm(sprayGun, cleaningSolution)', 
            'spraySurface(3047)', 
            'unloadArm()', 
            'loadArm(wiper)', 
            'wipeSurface(3047)', 
            'unloadArm()'
        ]
    ),
    (
        "The door handle needs to be disinfected",
        5059,
        2,
        [
            "loadArm(sprayGun, disinfectant)",
            "spraySurface(5059)",
            "unloadArm()",
            "loadArm(wiper)",
            "wipeSurface(5059)",
            "unloadArm()"
        ]
    ),
    (
        "The wall needs to be painted",
        1082,
        3,
        [
            "loadArm(sprayGun, paint)",
            "spraySurface(1082)",
            "unloadArm()",
            "loadArm(roller)",
            "spreadPaint(1082)",
            "unloadArm()"
        ]
    ),
    (
        "The crack on the wall needs to be filled with filler",
        1082,
        4,
        [
            "loadArm(sprayGun, filler)",
            "spraySurface(1082)",
            "unloadArm()",
            "loadArm(scraper)",
            "spreadFiller(1082)",
            "unloadArm()"
        ]
    ),
    (
        "The trashes on the floor need to be collected",
        3047,
        5,
        [
            "scanTrashes(3047)",
            "loadArm(gripper)",
            "collectTrashes()",
            "placeInTrashBag()",
            "unloadArm()"
        ]
    )
]

indirect_requests: List[Tuple[str, int, int, List[str]]] = [
    (
        "I dropped coffee on the floor",
        3047,
        1,
        [
            "loadArm(sprayGun, cleaningSolution)",
            "spraySurface(3047)",
            "unloadArm()",
            "loadArm(wiper)",
            "wipeSurface(3047)",
            "unloadArm()"
        ]
    ),
    (
        "The door handle is contaminated with germs",
        5059,
        2,
        [
            "loadArm(sprayGun, disinfectant)",
            "spraySurface(5059)",
            "unloadArm()",
            "loadArm(wiper)",
            "wipeSurface(5059)",
            "unloadArm()"
        ]
    ),
    (
        "The paint on the wall is worn out",
        1082,
        3,
        [
            "loadArm(sprayGun, paint)",
            "spraySurface(1082)",
            "unloadArm()",
            "loadArm(roller)",
            "spreadPaint(1082)",
            "unloadArm()"
        ]
    ),
    (
        "There is a crack on the wall",
        1082,
        4,
        [
            "loadArm(sprayGun, filler)",
            "spraySurface(1082)",
            "unloadArm()",
            "loadArm(scraper)",
            "spreadFiller(1082)",
            "unloadArm()"
        ]
    ),
    (
        "There are trashes on the floor",
        3047,
        5,
        [
            "scanTrashes(3047)",
            "loadArm(gripper)",
            "collectTrashes()",
            "placeInTrashBag()",
            "unloadArm()"
        ]
    )
]

different_height_requests: List[Tuple[str, int, int, List[str]]] = [
    (
        "The crack on the ceiling needs to be filled",
        2046,
        6,
        [
            "loadArm(scrapper, filler)",
            "polishSurface(2046)",
            "unloadArm()"
        ]
    ),
    (
        "The ceiling needs to be painted",
        2046,
        7,
        [
            "loadArm(roller, paint)",
            "rollSurface(2046)",
            "unloadArm()"
        ]
    )
]

multiple_tasks_requests: List[Tuple[str, List[int], int, List[str]]] = [
    (
        "The wall needs to be filled and painted",
        1082,
        9,
        [
            "loadArm(sprayGun, filler)",
            "spraySurface(1082)",
            "unloadArm()",
            "loadArm(scraper)",
            "spreadFiller(1082)",
            "unloadArm()",
            "loadArm(sprayGun, paint)",
            "spraySurface(1082)",
            "unloadArm()",
            "loadArm(roller)",
            "spreadPaint(1082)",
            "unloadArm()",
        ]
    ),
    (
        "The trash on the floor needs to be collected and then the wall needs to be painted",
        [3047, 1082],
        8,
        [
            "scanTrashes(3047)",
            "loadArm(gripper)",
            "collectTrashes()",
            "placeInTrashBag()",
            "unloadArm()",
            "loadArm(sprayGun, paint)",
            "spraySurface(1082)",
            "unloadArm()",
            "loadArm(roller)",
            "rollSurface(1082)",
            "unloadArm()"
        ]
    ),
    (
        "All windows in the room need to be cleaned and disinfected",
        [4019, 4036],
        10,
        [
            "loadArm(sprayGun, cleaningSolution)",
            "spraySurface(4019)",
            "spraySurface(4036)",
            "unloadArm()",
            "loadArm(sprayGun, disinfectant)",
            "spraySurface(4019)",
            "spraySurface(4036)",
            "unloadArm()",
            "loadArm(wiper)",
            "wipeSurface(4019)",
            "wipeSurface(4036)",
            "unloadArm()"
        ]
    )
]

requests = {
    "direct_requests": direct_requests,
    "indirect_requests": indirect_requests,
    "different_height_requests": different_height_requests,
    "multiple_tasks_requests": multiple_tasks_requests
}

def evaluate_robot_selection(requests, category_name, gpt_model: str = "gpt-4o"):
    """
    Evaluates the robot selection for a given set of requests.
    """
    correct_count = 0
    total_tests = 0
    robot_db = robots_withConfig

    print(f"Evaluating Robot Selection for {category_name}:\n")
    for idx, request in enumerate(requests):
        user_input = request[0]
        defect_id = request[1]
        ground_truth_robot_id = request[2]

        # Call select_robot function
        predicted_robot_id = select_robot(user_input, defect_id, robot_db, gpt_model)

        # Check if the predicted robot ID matches the ground truth
        is_correct_robot = predicted_robot_id == ground_truth_robot_id
        if is_correct_robot:
            correct_count += 1

        total_tests += 1

        # Output the results
        print(f"Test {idx + 1}: {user_input}")
        print(f"Predicted Robot ID: {predicted_robot_id}")
        print(f"Ground Truth Robot ID: {ground_truth_robot_id}")
        print(f"Robot Selection Result: {'Correct' if is_correct_robot else 'Incorrect'}\n")

    # Calculate accuracy for this category
    accuracy = (correct_count / total_tests) * 100
    print(f"{category_name} Robot Selection Accuracy: {accuracy:.2f}%\n")


def evaluate_robot_actions(requests, category_name):
    """
    Evaluates the robot actions for a given set of requests.
    """
    correct_count = 0
    total_tests = 0

    print(f"Evaluating Robot Actions for {category_name}:\n")
    for idx, request in enumerate(requests):
        user_input = request[0]
        defect_id = request[1]
        ground_truth_robot_id = request[2]
        ground_truth_actions = request[3]

        # Call get_repair_plan function
        predicted_actions = get_repair_plan(user_input, defect_id, ground_truth_robot_id)

        # Compare predicted actions with ground truth actions
        is_correct_actions = predicted_actions == ground_truth_actions
        if is_correct_actions:
            correct_count += 1

        total_tests += 1

        # Output the results
        print(f"Test {idx + 1}: {user_input}")
        print(f"Predicted Actions: {predicted_actions}")
        print(f"Ground Truth Actions: {ground_truth_actions}")
        print(f"Repair Plan Result: {'Correct' if is_correct_actions else 'Incorrect'}\n")

    # Calculate accuracy for this category
    accuracy = (correct_count / total_tests) * 100
    print(f"{category_name} Robot Actions Accuracy: {accuracy:.2f}%\n")


# Example of how to call these functions
# evaluate_robot_selection(direct_requests, "Direct Requests")
# evaluate_robot_actions(direct_requests, "Direct Requests")

# evaluate_robot_selection(indirect_requests, "Indirect Requests")
# evaluate_robot_actions(indirect_requests, "Indirect Requests")

# evaluate_robot_selection(different_height_requests, "Different Height Requests")
# evaluate_robot_actions(different_height_requests, "Different Height Requests")

# evaluate_robot_selection(multiple_tasks_requests, "Multiple Tasks Requests")
# evaluate_robot_actions(multiple_tasks_requests, "Multiple Tasks Requests")






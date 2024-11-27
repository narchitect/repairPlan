from planner.planner_navigation_o1 import get_navigationPath_o1
from planner.planner_a_start import a_star_path_planner
from utils.loader import GLOBAL_SCENE_GRAPH
import os
import random
from visualizer.vis_navigation import visualize_navigation
from data.robots2 import robots_withConfig

def is_valid_path(path, scene_graph_links):
    """
    Validates if the given path is possible within the scene graph.

    Parameters:
        path (list): The navigation path to validate (alternating room IDs and via IDs).
        scene_graph_links (list): The 'links' list from the scene graph.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    if not path or len(path) < 3:
        return False

    # Iterate over the path, stepping by 2 to handle room-via-room sequences
    for i in range(0, len(path) - 2, 2):
        current_room = path[i]
        via = path[i + 1]
        next_room = path[i + 2]


        # Check if a link exists connecting current_room and next_room via 'via'
        link_exists = False
        for link in scene_graph_links:
            if (
                via == link['via'] and
                current_room in link['spaces'] and
                next_room in link['spaces']
            ):
                link_exists = True
                break  # Link found, no need to search further

        if not link_exists:
            return False  # No valid link found for this segment

    return True  # All segments are valid


def evaluate_path_planner(trial_number, gpt_model):
    """
    Evaluates the LLM-based path planner against the A* path planner over a number of trials.

    Parameters:
        trial_number (int): The number of trials to run.
        gpt_model (str): The name or identifier of the GPT model to use.

    Returns:
        dict: A dictionary containing the success rate, average optimal score,
              and detailed results for each trial.
    """
    success_count = 0
    total_optimal_score = 0
    trial_results = []

    # Ensure directories for images exist
    a_star_dir = "/Users/nayunkim/Documents/GitHub/repairPlan/outputs/evaluation_path/a_star"
    path_planner_dir = "/Users/nayunkim/Documents/GitHub/repairPlan/outputs/evaluation_path/path_planner"
    os.makedirs(a_star_dir, exist_ok=True)
    os.makedirs(path_planner_dir, exist_ok=True)

    # Path to the input image for visualization
    input_image_path = "/Users/nayunkim/Documents/GitHub/repairPlan/data/images/top_view.png"

    for trial in range(1, trial_number + 1):
        # Load the global scene graph
        scene_graph = GLOBAL_SCENE_GRAPH

        # Randomly select start_room and target_room from 3 to 61, ensuring they are different
        start_room = robots_withConfig["robot_storage"]["room_id"]
        room_choices = [room for room in range(3, 62) if room != start_room]
        target_room = random.choice(room_choices)# 62 because the end value is exclusive

        # Get paths from both planners
        path = get_navigationPath_o1(target_room, scene_graph, gpt_model)
        path_a_star = a_star_path_planner(scene_graph, start_room, target_room)
        print(f"llm path: {path}")
        print(f"a* path: {path_a_star}")

        # Validate the LLM path
        if path and isinstance(path, list):
            is_valid = is_valid_path(path, scene_graph["links"])
            print(f"Path is valid: {is_valid}")
        else:
            is_valid = False

        # Initialize trial result
        trial_result = {
            'trial': trial,
            'start_room': start_room,
            'target_room': target_room,
            'success': False,
            'valid_path': is_valid,
            'optimal_score': 0.0,
            'path_length': len(path) if path else 0,
            'a_star_path_length': len(path_a_star) if path_a_star else 0,
            'path': path,
            'a_star_path': path_a_star
        }

        # Visualize the LLM-based path and save the image
        if path and isinstance(path, list):
            path_planner_image_output = f"{path_planner_dir}/trial_{trial}.jpg"
            visualize_navigation(
                path,                 # The navigation path
                None,                 # defect_id (set to None or appropriate value)
                scene_graph,          # The scene graph
                input_image_path,     # Input image path
                path_planner_image_output
            )

        # Visualize the A* path and save the image
        if path_a_star and isinstance(path_a_star, list):
            a_star_image_output = f"{a_star_dir}/trial_{trial}.jpg"
            visualize_navigation(
                path_a_star,
                None,
                scene_graph,
                input_image_path,
                a_star_image_output
        )

        # Check if the LLM path reaches the target room and is valid
        if is_valid and path[-1] == target_room:
            trial_result['success'] = True
            success_count += 1

            # Calculate optimal score, ensuring it does not exceed 1.0
            if len(path) > 0 and len(path_a_star) > 0:
                optimal_score = len(path_a_star) / len(path)
                optimal_score = min(1.0, optimal_score)  # Ensure the score does not exceed 1.0
            else:
                optimal_score = 0.0
            trial_result['optimal_score'] = optimal_score
            total_optimal_score += optimal_score
        else:
            # Failure case
            trial_result['optimal_score'] = 0.0

        trial_results.append(trial_result)

    # Calculate overall metrics
    success_rate = success_count / trial_number
    average_optimal_score = (total_optimal_score / success_count) if success_count > 0 else 0.0

    final_result = {
        'trial_number': trial_number,
        'gpt_model': gpt_model,
        'success_rate': success_rate,
        'average_optimal_score': average_optimal_score,
        'trial_results': trial_results
    }

    print(final_result)

    return final_result

# if __name__ == "__main__":
#     evaluate_path_planner(10, "gpt-4o")
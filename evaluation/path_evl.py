from planner.planner_navigation_o1 import get_navigationPath_o1
from planner.planner_a_start import a_star_path_planner
from utils.loader import GLOBAL_SCENE_GRAPH
import os
import random
from visualizer.vis_navigation import visualize_navigation
from data.robots2 import robots_withConfig

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
    a_star_dir = "outputs/evlaution_path/a_star"
    path_planner_dir = "outputs/evlaution_path/gpt4o_planner"
    os.makedirs(a_star_dir, exist_ok=True)
    os.makedirs(path_planner_dir, exist_ok=True)

    # Path to the input image for visualization (replace with your actual path)
    input_image_path = "./data/images/top_view.png"

    for trial in range(1, trial_number + 1):
        # Load the global scene graph
        scene_graph = GLOBAL_SCENE_GRAPH

        # Randomly select start_room and target_room from 3 to 61, ensuring they are different
        start_room = robots_withConfig["robot_storage"]["room_id"]
        target_room = random.sample(range(3, 62), 1)[0]  # 62 because the end value is exclusive
        print(f"start_room: {start_room}, target_room: {target_room}")

        # Get paths from both planners
        path = get_navigationPath_o1(target_room, scene_graph, gpt_model)
        path_a_star = a_star_path_planner(scene_graph, start_room, target_room)
        print(f"planner_path: {path}, a_star_path: {path_a_star}")

        # Initialize trial result
        trial_result = {
            'trial': trial,
            'start_room': start_room,
            'target_room': target_room,
            'success': False,
            'optimal_score': 0.0,
            'path_length': len(path) if path else 0,
            'a_star_path_length': len(path_a_star) if path_a_star else 0,
            'path': path,
            'a_star_path': path_a_star
        }

        # Visualize the LLM-based path and save the image
        if isinstance(path, list) and path:
            path_planner_image_output = f"{path_planner_dir}/trial_{trial}.jpg"
            visualize_navigation(
                path,                 # The navigation path
                None,                 # defect_id (set to None or appropriate value)
                scene_graph,          # The scene graph
                input_image_path,     # Input image path
                path_planner_image_output
            )

        # Visualize the A* path and save the image
        if isinstance(path_a_star, list) and path_a_star:
            a_star_image_output = f"{a_star_dir}/trial_{trial}.jpg"
            visualize_navigation(
                path_a_star,
                None,
                scene_graph,
                input_image_path,
                a_star_image_output
            )

        # Check if the LLM path reaches the target room
        if path and path[-1] == target_room:
            trial_result['success'] = True
            success_count += 1

            # Calculate optimal score
            if len(path) > 0 and len(path_a_star) > 0:
                optimal_score = len(path_a_star) / len(path)
            else:
                optimal_score = 0.0
            trial_result['optimal_score'] = optimal_score
            total_optimal_score += optimal_score
        else:
            # Failure case
            trial_result['optimal_score'] = 0.0
            print("path is empty")

        trial_results.append(trial_result)
        print(f"{trial}th trial is done")

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

if __name__ == "__main__":
    evaluate_path_planner(5, "gpt-4o")
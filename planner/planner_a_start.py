import heapq
import json
from utils.loader import load_scene_graph

def a_star_path_planner(scene_graph, start_room, target_room):
    # Parse the graph
    spaces = {space["id"]: space for space in scene_graph["nodes"]["spaces"]}
    links = scene_graph["links"]
    doors = {comp["id"]: comp for comp in scene_graph["nodes"]["components"] if comp["type"] == "door"}
    
    # Adjacency list to represent the graph
    graph = {space_id: [] for space_id in spaces}
    for link in links:
        room1, room2 = link["spaces"]
        door = link["via"]
        graph[room1].append((room2, door))
        graph[room2].append((room1, door))

    # Heuristic function: Euclidean distance between room centers
    def heuristic(room1, room2):
        loc1 = spaces[room1]["location"]
        loc2 = spaces[room2]["location"]
        return ((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2 + (loc1[2] - loc2[2])**2) ** 0.5

    # A* search
    open_set = []
    heapq.heappush(open_set, (0, start_room, [start_room]))
    g_score = {room: float("inf") for room in spaces}
    g_score[start_room] = 0

    while open_set:
        _, current_room, path = heapq.heappop(open_set)

        if current_room == target_room:
            return path  # Return the flattened sequence of [room_id, door_id, next_room_id]

        for neighbor, door in graph[current_room]:
            tentative_g_score = g_score[current_room] + 1  # Uniform cost for moving to a neighbor
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, target_room)
                heapq.heappush(open_set, (f_score, neighbor, path + [door, neighbor]))

    return None  # No path found


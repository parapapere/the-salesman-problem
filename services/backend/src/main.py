from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from itertools import permutations
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def tsp_solver(distance_matrix):
    print(distance_matrix)
    num_locations = distance_matrix.shape[0]
    location_indices = np.arange(num_locations)
    permutations_list = list(permutations(location_indices))

    shortest_route = None
    shortest_distance = float('inf')

    for permutation in permutations_list:
        total_distance = 0
        for i in range(num_locations - 1):
            current_location = permutation[i]
            next_location = permutation[i + 1]
            total_distance += distance_matrix[current_location, next_location]

        last_location = permutation[num_locations - 1]
        first_location = permutation[0]
        total_distance += distance_matrix[last_location, first_location]

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_route = permutation

    optimal_path = [location_indices[i] for i in shortest_route]
    optimal_path.append(location_indices[shortest_route[0]])

    return optimal_path, shortest_distance

@app.get("/")
def root():
   return {"message": "Welcome to the Architecture style API!"}

@ app.post("/count_optimal/")
async def get_net_image_prediction(user_distance_matrix: List[List[int]]):
    try:
        distance_matrix = np.array(user_distance_matrix)
        optimal_path, optimal_distance = tsp_solver(distance_matrix)
        # Convert numpy.int64 objects to int
        optimal_paths = [int(location) for location in optimal_path]
        optimal_distances = int(optimal_distance)

        # Encode the data to JSON format
        json_data = jsonable_encoder({"path": optimal_paths, "cost": optimal_distances})
        return JSONResponse(content=json_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


#This subscript was created by G. Jedrzejowski
#It outputs a JSON file named "points_new.json" which is supposed to be placed in the judge_rnaut/assets directory

import json
import os

filename = "json/points_new.json"

def write_json(data):
    # 1. Extract the directory path (e.g., "json")
    directory = os.path.dirname(filename)

    # 2. If the directory doesn't exist, create it
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    # 3. Check if file exists; if not, you can initialize it or just proceed to write
    if not os.path.exists(filename):
        print(f"{filename} not found. Creating a new file...")

    # 4. Write the data
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to {filename}: {e}")
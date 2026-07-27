from extract.api_client import get_data
from config.settings import DEFAULT_LIMIT
import json 
import os

def download_data(max_batches=None):
    os.makedirs("data/raw",exist_ok=True)
    batch_number = 1
    skip = 0
    while True:
        print(f"Downloading batch {batch_number}...")

        data = get_data(skip=skip)

        if len(data["results"]) == 0:
            print("No more records found.")
            print(f"Extraction completed. Total batches downloaded: {batch_number - 1}")
            break 

        file_path = f"data/raw/raw_{batch_number:04d}.json"
        with open(file_path,"w") as file:
            json.dump(data, file, indent=4)
        
        print(f"✓ Saved raw_{batch_number:04d}.json ({len(data['results'])} records)")

        if max_batches is not None and batch_number >= max_batches:
             print(f"Downloaded {max_batches} batches for testing.")
             break
        
        batch_number += 1
        skip += DEFAULT_LIMIT 
        

 #   data = get_data()
  # file_path = "data/raw/raw_0001.json"
  #  file_path = f"data/raw/raw_{batch_number:04d}.json"
   # with open(file_path, "w") as file:
    #    json.dump(data, file, indent=4)


# Import system functions that shouldn't need to be installed via pip
import uuid
import json

def add_history(current_time, query, results_list, prompt, response, elapsed_time, gpt3_temperature, gpt3_model):
  # generate a unique identifier for the entry
  entry_uuid = str(uuid.uuid4())

  # create the JSON entry
  entry = {
    "uuid": entry_uuid,
    "timestamp": current_time,
    "query": query,
    "query_results": results_list,
    "prompt": prompt,
    "completion": response,
    "elapsed_time": elapsed_time,
    "temp": gpt3_temperature,
    "model": gpt3_model
  }

  # open the data/ask_history.json file in read mode
  with open('static/data/ask_history.json', 'r') as f:
    try:
      # read the contents of the file
      history = json.load(f)
    except json.decoder.JSONDecodeError:
      # if the file is empty or not a valid JSON file, initialize the history with an empty list
      history = []

  # prepend the new entry to the beginning of the history list
  history.insert(0, entry)

  # open the data/ask_history.json file in write mode
  with open('static/data/ask_history.json', 'w') as f:
    # write the updated history to the file
    json.dump(history, f, indent=2)
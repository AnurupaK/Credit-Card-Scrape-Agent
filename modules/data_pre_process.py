import json
import re
import pandas as pd

# Function to pre-process the raw card content and convert it into structured card details
def card_pre_process(card_content):
    card_details_list = []
    try:
        for card_index in range(len(card_content)):
            raw = card_content[card_index]
            # Regular expression to filter out unwanted lines
            pattern = r'[^```,json,\n].*'
            lines = re.findall(pattern, raw)
            json_str = "\n".join(lines)
            
            # Convert the cleaned JSON string into a Python dictionary
            card_details = json.loads(json_str)
            card_details_list.append(card_details)
        
        return card_details_list
    except Exception as e:
        print(e)

# Function to convert card details into a CSV-compatible format (Pandas DataFrame)
def make_csv(cards_info):
    try:
        cleaned_data = [{k: str(v) for k, v in card.items()} for card in cards_info]
        
        df = pd.DataFrame(cleaned_data)

        return df
    except Exception as e:
        print(e)

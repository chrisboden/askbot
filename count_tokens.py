import csv
import os
from transformers import GPT2TokenizerFast

def calculate_tokens(file_path):
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    num_tokens = 0

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the CSV file and read the rows
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                quote_text = row['quoteText']
                tokens = tokenizer(quote_text)['input_ids']
                num_tokens += len(tokens)
    else:
        print(f'Error: file "{file_path}" does not exist.')

    return num_tokens

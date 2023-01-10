# Import programs that are installed via pip
import openai
from transformers import GPT2TokenizerFast
from pathlib import Path

# Import system functions that shouldn't need to be installed via pip
import os

# Variables that can be tweaked

gpt3_model = "text-davinci-003"
gpt3_temperature = 0.2
max_allowable_tokens = 4096

# Completions function for passing the prompt plus the query results to openai's completions api and having it synthesise and return a result

def completions(user_input, results_list):
    # Read the contents of the prompt.txt file and assign it to a string variable
    with open(Path("prompt_template.txt"), "r") as f:
        prompt_text = f.read()

    # Convert the results_list variable to a single string
    results_list = "\n".join(results_list)

    # Initialize the tokenizer
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    # Tokenize the results_list string
    results_list_tokens = tokenizer.encode(results_list)

    # Get the number of tokens in the results_list
    context_length = len(results_list_tokens)
    # print(f"The context length is {context_length}")

    # Truncate the results_list string at the end of the nearest sentence
    if context_length > 2500:
        for i, token in enumerate(results_list_tokens):
            if token == tokenizer.encode(".")[0] and i < 2500:
                results_list = tokenizer.decode(results_list_tokens[:i+1])
                break

    # Build the prompt string using the prompt_text, user_input and results
    prompt = f"{prompt_text}\n\nContext:\n{results_list}\n\nQ: {user_input}\nA:"
    # print(f"Prompt is: {prompt}")

    # Tokenize the prompt string
    prompt_tokens = tokenizer.encode(prompt)

    # Get the number of tokens in the prompt
    prompt_tokens_count = len(prompt_tokens)
    # print(f"The total prompt tokens is {prompt_tokens_count}")

    # Calculate the max_tokens value
    max_tokens = max_allowable_tokens - prompt_tokens_count
    # print(f"The max tokens remaining is {max_tokens}")

    # Call the OpenAI API with the prompt
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.Completion.create(
        model=gpt3_model,
        prompt=prompt,
        top_p=0,
        n=1,
        max_tokens=max_tokens,
        echo=False,
        temperature=gpt3_temperature
    )

    print(completion)

    # We ask for a bunch of things to be returned so that they can be used in the askapp.py file, eg in the search function where we call the addhistory function to add to the json file.

    return completion, prompt_tokens_count, context_length, prompt, max_tokens, results_list, gpt3_temperature, gpt3_model
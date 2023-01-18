# Import programs that are installed via pip
import openai
from transformers import GPT2TokenizerFast
from pathlib import Path
import dotenv

# Import system functions that shouldn't need to be installed via pip
import os

# Variables that can be tweaked

gpt3_model = "text-davinci-003"
gpt3_top_p = 1
gpt3_temperature = 0.00
max_allowable_tokens = 4096


# Set up the various file path variables so that the paths are relative no matter the environment
cwd = Path(__file__).parent.resolve()
prompt_txt_path = cwd.joinpath('prompt_template.txt')


# Completions function for passing the prompt plus the query results to openai's completions api and having it synthesise and return a result

def completions(user_input, results_list):
    with open(prompt_txt_path, "r") as f:
        prompt_text = f.read()

    results_list = "\n".join(results_list)

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    results_list_tokens = tokenizer.encode(results_list)

    context_length = len(results_list_tokens)

    if context_length > 2500:
        for i in range(len(results_list_tokens)-1, -1, -1):
            if results_list_tokens[i] == tokenizer.encode(".")[0] and i < 2500:
                results_list = tokenizer.decode(results_list_tokens[:i+1])
                break

    prompt = f"{prompt_text}\n\nQUOTES:\n{results_list}\n\nQ: {user_input}\nA:"

    prompt_tokens = tokenizer.encode(prompt)

    prompt_tokens_count = len(prompt_tokens)

    max_tokens = max_allowable_tokens - prompt_tokens_count

    # Call the OpenAI API with the prompt
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.Completion.create(
        model=gpt3_model,
        prompt=prompt,
        top_p=gpt3_top_p,
        n=1,
        max_tokens=1088,
        echo=False,
        temperature=gpt3_temperature
    )

    print(completion)

    # We ask for a bunch of things to be returned so that they can be used in the askapp.py file, eg in the search function where we call the addhistory function to add to the json file.

    return completion, prompt_tokens_count, context_length, prompt, max_tokens, results_list, gpt3_temperature, gpt3_model
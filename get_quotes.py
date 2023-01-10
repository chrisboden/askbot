# Import programs that are installed via pip
from pyppeteer import launch
from bs4 import BeautifulSoup
from langdetect import detect_langs
import asyncio
from pathlib import Path

# Import system functions that shouldn't need to be installed via pip
import csv
import os
import re

# Import from other python files in our code

# Import the calculate_tokens function from the tokens module
from count_tokens import calculate_tokens
# Import the scrape_quotes function from the scrapequotes module
from scrape_quotes import scrape_quotes

async def main(url):
    # Use the scrape_quotes function
    quotes = await scrape_quotes(url)

# Prompt the user for the author name and book title
author = input("Enter the author's name: ")
book_title = input("Enter the book title: ")

# Substitute the user-provided values in the URL
url = f'https://www.goodreads.com/quotes/search?commit=Search&q={ "+".join(author.split()) }+{ "+".join(book_title.split()) }'

# Print the final URL that will be scraped
print(f'Final URL to be scraped: {url}')

# Call the scrape_quotes function and pass in the URL of the Goodreads author profile page
quotes = asyncio.get_event_loop().run_until_complete(scrape_quotes(url))

# Check if file exists
file_path = Path(f'data/scrapes/{author}_{book_title}.csv')
if not file_path.exists():
    open(file_path, 'w').close()


# Create a set to store the quotes
quote_set = set()

# Import the savecsv function from the savecsv file
import save_csv as qc

qc.write_quotes_to_csv(quotes, file_path)

# Call the calculate_tokens function and assign the result to the num_tokens variable
num_tokens = calculate_tokens(file_path)

# Calculate the cost of embedding the tokens
cost = (num_tokens / 1000) * 0.0004

print(f'There are {num_tokens} tokens in this file.')
print(f'It will cost ${cost:.5f} to embed these tokens using OpenAI')

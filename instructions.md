##Scraping Quotes

To scrape quotes from goodreads, run getquotes.py from the command line.
You will be prompted for an author and title, enter those and hit return.
The script will scrape quotes for that title/author combination until it finishes. 
The scraped quotes are saved to a file in /scrapes directory called {authorName}_{bookTitle}.csv
The script calculates the number of tokens in the file and computes the cost to get the openai embeddings.


## Get OpenAI Embeddings for quotes

Before you do this you should export your OPENAI_API_KEY as an env variable and make sure you have some credit in your OpenAI account.

To get the OpenAI embeddings for the quotes, run the quote_embed.py file. It will grab any csv in the /scrapes directory and iterate through each row to get an embed for the quotetext, bookTitle and bookAuthor as a concatenated string as follows: {quote_text} | From: {book_title} | By: {book_author}.

The script adds the embeddings plus the other fields (which are treated as metadata) to a file called base.csv in the /embeds directory.


You'll need to open the terminal
Navigate to the directory using cd command

Step 1:
Install the programs in requirements.txt 
pip install requirements.txt

Step 2:
Run this command:
export FLASK_APP=main

Step 3:
Run this command to export your OPENAI api key:
export OPENAI_API_KEY=blah
(You'll need to get your key from the openai acount dashboard)

Step 4:
Run this command to start the app:
flask run



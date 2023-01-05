import asyncio
import csv
import os
import re
from pyppeteer import launch
from bs4 import BeautifulSoup
from langdetect import detect_langs

async def scrape_quotes(url):
    # Launch pyppeteer and create a new browser instance
    browser = await launch()
    page = await browser.newPage()

    # Initialize an empty list to store the quotes
    quotes = []
    page_num = 1
    max_pages = 1  # Set default value for max_pages

    while page_num <= max_pages:
        # Navigate to the URL for the current page
        await page.goto(f'{url}&page={page_num}',{'waitUntil' : 'networkidle0'})

        # Find the span element with class "smallText" inside an h3 element
        small_text = await page.evaluate('''() => {
            const h3 = document.querySelector('h3');
            return h3.querySelector('.smallText').innerText;
        }''')

        # Use a regular expression to extract the number after "of "
        match = re.search(r'of (\d+,?\d*)', small_text)
        print(small_text)
        if match:
            number_str = match.group(1)
            number_str = number_str.replace(',', '')  # Replace the comma with an empty string
            number = int(number_str)

            # Calculate the maximum number of pages
            quotes_per_page = 20
            max_pages = (number // quotes_per_page) + 1
            if max_pages > 100:
                max_pages = 100

        # Evaluate a JavaScript expression to get the quotes on the page
        try:
            page_quotes = await page.evaluate('''() => {
                const quotes = [];
                const quoteElements = document.querySelectorAll('.quoteDetails');
                for (const element of quoteElements) {
                    let quoteText, bookAuthor, bookTitle, tags;
                    try {
                        quoteText = element.querySelector('div.quoteText').firstChild.textContent.trim();
                        bookAuthor = element.querySelector('div.quoteText span.authorOrTitle').innerText.trim();
                        bookTitle = element.querySelector('div.quoteText a[href*="/work/quotes"]').innerText.trim();
                        tags = Array.from(element.querySelectorAll('.greyText a'))
                            .map(tag => tag.innerText.trim());
                    } catch (e) {
                        // If an error occurs, skip adding this quote to the list
                        continue;
                    }
                    quotes.push({ quoteText, bookAuthor, bookTitle, tags });
                }
                return quotes;
            }''')
        except Exception as e:
            # If an error occurs, print an error message and skip adding the item to the CSV
            print(f'Error occurred while trying to find DOM element: {e}')
            continue

        # Add the quotes from the page to the list of all quotes
        for quote in page_quotes:
            quoteText = quote['quoteText']
            bookTitle = quote['bookTitle']
            bookAuthor = quote['bookAuthor']
            try:
                languages = detect_langs(quoteText)
                if 'en' in [lang.lang for lang in languages]:
                    quotes.append({'quoteText': quoteText, 'bookTitle': bookTitle, 'bookAuthor': bookAuthor, 'tags': quote['tags']})
            except Exception as e:
                # Handle the error here. For example, you could log the error message.
                print(f'Error occurred while detecting language for quote: {quoteText}. Error message: {e}')


        # Print a message indicating that the page was scraped successfully
        print(f'Scraped page {page_num} successfully')

        # Increment the page number
        page_num += 1

    # Close the browser
    await browser.close()

    return quotes
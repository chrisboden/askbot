import csv

quote_set = set()

def write_quotes_to_csv(quotes, file_path):
    # Write the quotes to a CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['quoteText', 'bookTitle', 'bookAuthor', 'tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for quote in quotes:
            # Strip any trailing commas and quote marks from the fields
            quote['quoteText'] = quote['quoteText'].rstrip(',').strip('“').strip('”')
            quote['bookTitle'] = quote['bookTitle'].rstrip(',')
            quote['bookAuthor'] = quote['bookAuthor'].rstrip(',')

            # Check if the length of the quote is greater than 3000 or less than 50
            if len(quote['quoteText']) > 3000 or len(quote['quoteText']) < 50:
                # Skip writing the quote to the CSV file if it is too long or too short
                continue

            # Check if the quote is already in the set
            if quote['quoteText'] not in quote_set:
                # Add the quote to the set
                quote_set.add(quote['quoteText'])

                # Write the quote to the CSV file
                writer.writerow(quote)
# Required libraries
import requests
from selectolax.parser import HTMLParser
import pandas as pd

# The URL to scrape data from marketwatch's list of Companies
url = "https://www.marketwatch.com/tools/markets/stocks/a-z/A"

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Parse the response content using HTMLParser from selectolax
tree = HTMLParser(response.content)

# Target the table with the specified class that contains stock information
table = tree.css("table[class ='table table-condensed']")
title_list = []

# Iterate through the table content
for table_node in table:
    # Extract column headers from the table
    heading = table_node.css("thead > tr > th")
    for head in heading:
        title_list.append(head.text())

    # Construct a dictionary to store the scraped data
    stocks_info = {
        title_list[0]: [title.text().split("(")[0] for title in table_node.css("tbody > tr > td[class='name'] > a")],
        "Ticker": [ticker.text().split("(")[1].split(")")[0] for ticker in table_node.css("tbody > tr > td[class='name'] > a")],
        title_list[1]: [country.text() for country in table_node.css("tbody > tr > td:nth-child(2)")],
        "Country Code": [url.attributes['href'].split("=")[1] for url in table_node.css("tbody > tr > td[class='name'] > a")],
        title_list[2]: [exchange.text() for exchange in table_node.css("tbody > tr > td:nth-child(3)")],
        title_list[3]: [sector.text() for sector in table_node.css("tbody > tr > td:nth-child(4)")],
        "More Info": ["https://www.marketwatch.com/" + url.attributes['href'] for url in table_node.css("tbody > tr > td[class='name'] > a")]
    }


# Convert the dictionary to a DataFrame
df = pd.DataFrame(stocks_info, columns=stocks_info.keys())
# Save the DataFrame to a CSV file
df.to_csv("Stock_info.csv", index=False)

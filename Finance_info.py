# Required imports
import requests
from selectolax.parser import HTMLParser
import pandas as pd

# Convert financial units into a standardized format
def convert_to_units(x):
    x = str(x).strip()
    # Handling for empty or 'N/A' strings
    if x in ('', '-', ' ', 'N/A'):
         return "-"
    # Conversion for Billion
    elif 'B' in x:
        return str(float(x.replace('(', "").replace(')', "").strip('B')) * (-1 if '(' in x and ')' in x else 1)) + "B"
    # Conversion for Million
    elif 'M' in x:
        return str(float(x.replace('(', "").replace(')', "").strip('M')) * (-1 if '(' in x and ')' in x else 1)) + "M"
    # Conversion for Thousand
    elif 'K' in x:
        return str(float(x.replace('(', "").replace(')', "").strip('K')) * (-1 if '(' in x and ')' in x else 1)) + "K"
    # Conversion for Percentage
    elif '%' in x:
        return str(float(x.replace(',', "").replace('(', "").replace(')', "").strip('%')) * (-1 if '(' in x and ')' in x else 1)) + "%"
    # Default case
    else:
        return float(x.replace('(', "").replace(')', ""))

# Function to divide a list into smaller chunks of size n
def chunk(values, n):
    for i in range(0, len(values), n):
        yield values[i:i + n]

# Generate URL for given stock ticker, financial statement, and country code
def get_financial_info_url(ticker, finance, countrycode):
    return f"https://www.marketwatch.com/investing/stock/{ticker}/financials/{finance}?countrycode={countrycode}&mod=mw_quote_tab"

# Fetch and parse the HTML content from a given URL
def get_html_tree(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "You are not allowed to Web Scrap at this time"
    else:
        return HTMLParser(response.content)

# Extract financial information from the parsed HTML
def get_fininfo_from(table_nodes):
    # Extracting year headers
    years = [year.text() for year in table_nodes.css("thead > tr > th[class = 'overflow__heading'] > div")]
    # Extracting financial information
    fin_info = {
        "item": [heading.text() for heading in table_nodes.css("tbody > tr > td[class='overflow__cell fixed--column'] > div[class*='cell__content fixed']")],
        "value": [convert_to_units(heading.text()) for heading in table_nodes.css("tbody > tr > td[class='overflow__cell'] > div:nth-child(1)")]
    }
    # Splitting values into chunks for each year
    fin_info["value"] = list(chunk(fin_info["value"], 6))
    return fin_info, years

# Convert extracted financial information into a DataFrame
def generate_dataframe(fin_info, years):
    temp_df = pd.DataFrame(fin_info)
    value_df = pd.DataFrame(temp_df['value'].tolist(), columns=years)
    return pd.concat([temp_df.drop('value', axis=1), value_df.drop('5-year trend', axis=1)], axis=1)

# Get the company name for a given stock ticker
def get_company_name_by_ticker(ticker):
    df = pd.read_csv('Stock_info/Stock_info.csv')
    return df.loc[df['Ticker'] == ticker, 'Name'].values[0]

# Main function to fetch and save financial information
def get_fininfo_for(ticker, finance, countrycode):
    url = get_financial_info_url(ticker, finance, countrycode)
    tree = get_html_tree(url)
    tables = tree.css("table[class='table table--overflow align--right'")
    df = pd.DataFrame()
    for table_nodes in tables:
        fin_info, years = get_fininfo_from(table_nodes)
        temp_df = generate_dataframe(fin_info, years)
        df = df._append(temp_df, ignore_index=True)
    if df.empty:
        print("No information available or incorrect input provided.")
    else:
        df.to_csv(f"{get_company_name_by_ticker(ticker)}-{finance} statement.csv")

# Starting point of the script
if __name__ == '__main__':
    get_fininfo_for("533292", "income", "IN")

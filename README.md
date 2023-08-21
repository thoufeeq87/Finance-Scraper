# 📈 Finance Scraper 🌍

This project contains two Python scripts designed to scrape financial data from [MarketWatch](https://www.marketwatch.com/). It fetches financial information for specified stocks as well as a comprehensive list of company information.

## 📂 Files in this Project

1. `Finance_info.py`: Extracts financial data for a specified stock.
2. `Stock_info.py`: Fetches a list of stocks and relevant information.
3. `Stock_info.csv`: Contains the scraped list of stocks with their details.

## 💼 Finance_info.py

This script is designed to extract detailed financial information for a given stock ticker.

### How it works:
- Uses the `requests` library to fetch the webpage content.
- Parses the content using `selectolax.parser`'s `HTMLParser`.
- Processes financial data and exports the final information into a CSV file.

#### Usage:
```bash
python Finance_info.py
```
**This script, as currently written, fetches the income statement for the stock ticker "533292" registered in India ("IN").**

## 🛠 Customizing Data Extraction in `Finance_info.py`

The `Finance_info.py` script provides flexibility in fetching different types of financial statements for various stock tickers. By default, the script might be set to fetch a specific statement for a specific ticker using the `get_fininfo_for()` function.

### 1. **Stock Ticker**: 
- Open the `Finance_info.py` file.
- In the line `if __name__ == '__main__': get_fininfo_for("533292", "income", "IN")`, the first argument represents the stock ticker. 
- Replace `"533292"` with the desired stock ticker. 
- For a list of available tickers, refer to the `Stock_info.csv` file.

### 2. **Type of Financial Statement**:
Options include:
   - **Income Statement**: Use the value `"income"`
   - **Balance Sheet**: Use the value `"balance-sheet"`
   - **Cash Flow Statement**: Use the value `"cash-flow"`

In the line `if __name__ == '__main__': get_fininfo_for("533292", "income", "IN")`, replace the `"income"` argument with one of the options mentioned above.

### 3. **Country Where the Stock is Located**: 
- In the line `if __name__ == '__main__': get_fininfo_for("533292", "income", "IN")`, the third argument represents the country where the stock is located. 
- Replace `"IN"` with the desired country code.
- For a list of valid country codes, refer to the `Stock_info.csv` file.

After making the necessary adjustments, run the script again to fetch the desired financial data.


## 📊 Stock_info.py

This script is designed to extract a list of stocks with their details.

### How it works:
- Uses the `requests` library to fetch the webpage content.
- Parses the content using `selectolax.parser`'s `HTMLParser`.
- Extracts stock details and exports the final list into a CSV file named `Stock_info.csv`.

### Usage:
  ```bash
  python Stock_info.py
   ``` 
The generated `Stock_info.csv` contains the following columns:
- Name
- Ticker
- Country
- Country Code
- Exchange
- Sector
- More Info (Link to MarketWatch's stock detail page)

## 📌 Dependencies
- `requests`
- `selectolax`
- `pandas`
## 🚀 Getting Started

1. Clone this repository:
  ```bash
  git clone https://github.com/thoufeeq87/Finance-Scraper.git
  ```
2. Install the required dependencies:
  ```bash
  pip install requests selectolax pandas
  ```
3. Run the desired script:
  ```bash
  python Finance_info.py
  python Stock_info.py
  ```
👩‍💻 Happy coding and data scraping! 👨‍💻

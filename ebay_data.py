import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup, productlist):
    results = soup.find_all('div', {'class': 's-item__wrapper clearfix'})

    for item in results:
        subtitles = item.find_all('div', {'class': 's-item__subtitle'})
        subtitle_texts = [subtitle.text for subtitle in subtitles]

        product = {
            'title': item.find('div', {'class': 's-item__title'}).text,
            'itemConditions': subtitle_texts,
            'price': item.find('span', {'class': 's-item__price'}).text,
            'soldQuantity': getattr(item.find('span', {'class': 's-item__dynamic s-item__quantitySold'}), 'text', None)
        }
        print(product)
        productlist.append(product)

def output(productlist):
    df = pd.DataFrame(productlist)
    df.to_csv('output.csv', index=False)
    df.to_excel('output.xlsx', index=False)

# Initialize an empty list to store data
productlist = []

# Loop through pages 1 to 5
for page_number in range(1, 21):
    page_url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw=laptop&_sacat=0&_pgn={page_number}'
    
    # Get data from the current page
    soup = get_data(page_url)
    
    # Parse the data and add to productlist
    parse(soup, productlist)

# Output the data to CSV and Excel
output(productlist)

--------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=laptop&_sacat=0&_pgn=1'

def get_data(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup

productlist = []

def parse(soup):
  results = soup.find_all('div', {'class': 's-item__wrapper clearfix'})
  productlist.clear()

  for item in results:
    subtitles = item.find_all('div', {'class': 's-item__subtitle'})
    subtitle_texts = [subtitle.text for subtitle in subtitles]

    product = {
        'title': item.find('div', {'class': 's-item__title'}).text,
        'itemConditions': subtitle_texts,
        'price': item.find('span', {'class': 's-item__price'}).text,
        'soldQuantity': getattr(item.find('span', {'class': 's-item__dynamic s-item__quantitySold'}), 'text', None)
    }
    print(product)
    productlist.append(product)
  return productlist

def output(productlist):
  df = pd.DataFrame(productlist)
  df.to_csv('output.csv', index=False)
  df.to_excel('output.xlsx', index=False)
  return

soup = get_data(url)
parse(soup)
output(productlist)

---------------------------------------------------------
data = pd.read_csv('/content/outputTest.csv')

# Replace NaN values in the 'soldQuantity' column with 0
data['soldQuantity'].fillna(0, inplace=True)

# Define a function to split non-"0" values
def split_quantity(value):
  if value == 0:
    return 0
  else:
    parts = value.split(" ")
    return parts[0]

# Apply the function to 'soldQuantity' column
data['soldQuantity'] = data['soldQuantity'].apply(split_quantity)

# Remove the '+' symbol from 'soldQuantity' values
data['soldQuantity'] = data['soldQuantity'].str.replace('+', '', regex=True)

data['soldQuantity'].fillna(0, inplace=True)
data['soldQuantity'].values

-------------------------------------------------------------
# Drop rows where 'price' column contains the specified string
data = data[data['price'] != 'Tap item to see current priceSee price']

def extract_middle_value(price_range):
    print(price_range)
    # Split the price range by 'to'
    prices = price_range.split(' to ')
    
    # Convert the prices to floats
    prices = [float(price.replace('$', '')) for price in prices]
    
    # Calculate the middle value
    middle_value = sum(prices) / len(prices)
    print(middle_value)
    
    return middle_value

# Apply the function to the 'price' column
data['price'] = data['price'].apply(lambda x: extract_middle_value(x) if ' to ' in str(x) else x)

# Remove the '$' symbol from the 'price' column only if it exists
data['price'] = data['price'].apply(lambda x: x.replace('$', '') if isinstance(x, str) and '$' in x else x)

--------------------------------------------------------------------
# Define a function to check if 'Brand New' is present anywhere in the array
def condition_to_numeric(item_condition):
    return 0 if any('Brand New' in condition for condition in item_condition) else 1

# Apply the function to the 'itemCondition' column
data['itemConditions'] = data['itemConditions'].apply(lambda x: condition_to_numeric(eval(x)) if isinstance(x, str) else x)

----------------------------------------------------------------------
import numpy as np

def extract_laptop_brand(product_title, brand_names):
    for brand in brand_names:
        if brand in product_title:
            return brand
    return np.nan  # Return np.nan if no brand is found

# List of known brand names
brand_names = ['HP', 'SGIN', 'ASUS', 'Dell', 'DELL', 'Fujitsu', 'MSI', 'CHUWI', 'Microsoft', 'Panasonic', 'Acer', 'Lenovo']

# Apply the function to create a new column 'brand' in the DataFrame
data['brand'] = data['title'].apply(lambda x: extract_laptop_brand(x, brand_names))

# Drop rows where 'brand' is NaN
data.dropna(subset=['brand'], inplace=True)

------------------------------------------------------------------
import re

# Define a regular expression pattern to extract the screen size
screen_size_pattern = r'(\d+(\.\d+)?)\s*"'  # Matches digits with optional decimal followed by a space and double quote

# Iterate through the DataFrame and store screen size in a new column 'screen_size'
data['screen_size'] = data['title'].apply(lambda x: re.search(screen_size_pattern, x).group(1) if re.search(screen_size_pattern, x) else None)

# Convert the 'screen_size' column to numeric (optional)
data['screen_size'] = pd.to_numeric(data['screen_size'], errors='coerce')
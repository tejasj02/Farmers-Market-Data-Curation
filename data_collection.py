import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin
import pandas as pd
import censusdata
import regex as re


# get census data
def fetch_census_data():
    
    geo = censusdata.censusgeo([('state', '37'), ('zip code tabulation area', '*')])

    # fetch data: total population, median income, age groups
    data = censusdata.download(
        src='acs5',  
        year=2019,  
        geo=geo,   
        var=['B01003_001E', 'B19013_001E', 'B01001_007E', 'B01001_008E', 'B01001_009E', 'B01001_010E', 
             'B01001_011E', 'B01001_031E', 'B01001_032E', 'B01001_033E', 'B01001_034E', 'B01001_035E']
    )
    # Add ZIP codes as a column
    data['zipcode'] = data.index.map(lambda x: x.geo[1][1])
    data['pop_18_30'] = ( data['B01001_007E'] + data['B01001_008E'] + data['B01001_009E'] + data['B01001_010E'] + 
                         data['B01001_011E'] + data['B01001_031E'] + data['B01001_032E'] + data['B01001_033E'] + 
                         data['B01001_034E'] + data['B01001_035E'])
    data.rename(columns={
    'B01003_001E': 'total_population',  # Total population
    'B19013_001E': 'median_income',     # Median household income
    }, inplace=True)
    data = data[['zipcode', 'total_population', 'median_income', 'pop_18_30']]
    return data.reset_index(drop=True)

# Requesting a page
def request_page(url):
    try:
        # Setting a User-Agent header to mimic a browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response
        else:
            print(f"Failed to fetch the page, Status Code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

# extract market details from each page
def extract_market_details(page_soup):
    markets = []
    
    # find the table layout type
    table = page_soup.find('table', {'cellpadding': '4'})
    if not table:
        print("Table with cellpadding=4 not found on this page.")
        return markets

    # find rows in table
    table_rows = table.find_all('tr')

    for row in table_rows:
        td_elements = row.find_all('td')  # find item in row
        
        if td_elements:
            
            for td in td_elements: # extract market information in item
                market_info = {}
                
                name_tag = td.find('span', class_='style1')
                if name_tag:
                    market_info['name'] = name_tag.get_text(strip=True)
                
                # look for address
                address_parts = []
                address_p_tag = td.find('p', align='left')
                if address_p_tag:
                    # find the first <a> tag (start capturing after this tag)
                    start_address = False
                    for element in address_p_tag.find_all(string=True, recursive=True):  
                        if element.parent.name == 'a':  
                            start_address = True
                            continue  
                        if start_address:
                            if element.parent.name == 'strong' or element.parent.name == 'a':  
                                break
                            if element.strip():
                                # replace non-breaking spaces (\xa0) with regular spaces
                                address_parts.append(element.strip().replace('\xa0', ' '))
                    
                market_info['address'] = " ".join(address_parts).strip() if address_parts else None
                
                # search for "Office Phone"
                office_phone_tag = td.find(string=lambda text: text and 'Office Phone' in text)
                if office_phone_tag:
                    office_phone_number = office_phone_tag.find_next('br').previous_sibling.strip()  # Get the phone number
                    market_info['office_phone'] = office_phone_number
                else:
                    market_info['office_phone'] = None
                
                # search for "Home Phone"
                home_phone_tag = td.find(string=lambda text: text and 'Home Phone' in text)
                if home_phone_tag:
                    home_phone_number = home_phone_tag.find_next('br').previous_sibling.strip()  # Get the phone number
                    market_info['home_phone'] = home_phone_number
                else:
                    market_info['home_phone'] = None
                
                # look for website 
                website_tag = td.find('a', href=True, string='Web Site')
                if website_tag:
                    market_info['website'] = website_tag['href']
                else:
                    market_info['website'] = None
                
                markets.append(market_info)

    return markets

# cumulate markets and switch pages
def fetch_all_markets(base_url):
    all_markets = []
    current_page = 1

    while True:
        print(f"Fetching page {current_page}...")

        # construct the URL for the current page
        page_url = f"{base_url}&page={current_page}"

        response = request_page(page_url)
        if not response:
            break  # stop if the page couldn't be fetched

        page_soup = BeautifulSoup(response.text, 'html.parser')

        # extract market details from this page
        markets = extract_market_details(page_soup)
        all_markets.extend(markets) 

        # next page
        next_page = page_soup.find('a', string='[Next >]')
        if next_page and 'href' in next_page.attrs:
            
            next_url = next_page['href']
            next_url = urljoin(base_url, next_url) 
            print(f"Next page URL: {next_url}")
            current_page += 1
        else:
            print("No next page found. Exiting.")
            break 

        # add a delay to prevent overloading the server
        time.sleep(random.uniform(2, 4)) 

    return all_markets

# Main function, fetch data, merge, and save to csv
if __name__ == "__main__":
    base_url = "https://www.ncfarmfresh.com/directory.asp?product=17&SearchType=farmmarkets"  # Base URL without the page number

    # fetch census data
    print("Fetching Census data...")
    census_data = fetch_census_data()

    # fetch farmers' market data
    print("Fetching Farmers' Market data...")
    base_url = "https://www.ncfarmfresh.com/directory.asp?product=17&SearchType=farmmarkets"
    markets = fetch_all_markets(base_url)

    market_df = pd.DataFrame(markets)
    market_df['zipcode'] = market_df['address'].apply(lambda x: re.search(r'\b\d{5}\b', x).group(0) if re.search(r'\b\d{5}\b', x) else None)
    # merge
    print("Merging datasets...")
    merged_data = pd.merge(market_df, census_data, on='zipcode', how='left')

    # Save to CSV
    merged_data.to_csv('market_data.csv', index=False)
    print("Merged data saved to 'market_data.csv'")
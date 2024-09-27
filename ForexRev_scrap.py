import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import html
from datetime import datetime
from datetime import date

# Define the clean_text function
def clean_text(text):
    # Remove HTML tags
    clean = re.sub(r'<.*?>', '', str(text))
    # Decode HTML entities and fix encoding issues
    clean = html.unescape(clean)
    clean = clean.replace('Â', ' ').replace('\xa0', ' ').strip()
    return clean

# Define the extract_dates function
def extract_dates(dates_string):
    dates_list = re.findall(r'\d{2}\.\d{2}\.\d{4}', dates_string)
    return ', '.join(dates_list) if dates_list else dates_string.strip()

# Fetch the web page
url = "This data was deleted for safety reasons"
response = requests.get(url)
response.encoding = 'utf-8'  # Ensure correct encoding
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

# Parse the HTML for the data
script = soup.find('script', string=re.compile("svtPublic"))
script_content = script.string

# Extract the relevant parts using regex
data_pattern = re.compile(r"svtPublic\[\d+\]\['data'\] = '(.*?)';")
brand_pattern = re.compile(r"svtPublic\[\d+\]\['nazwa_podmiotu'\] = '(.*?)';")
website_pattern = re.compile(r"svtPublic\[\d+\]\['strona_www'\] = '(.*?)';")
case_authority_pattern = re.compile(r"svtPublic\[\d+\]\['organ_wydajacy_ostrzezenie'\] = '(.*?)';")

dates = data_pattern.findall(script_content)
brands = brand_pattern.findall(script_content)
websites = website_pattern.findall(script_content)
case_authorities = case_authority_pattern.findall(script_content)

# Clean the data
dates = [extract_dates(clean_text(date)) for date in dates]
brands = [clean_text(brand) for brand in brands]
websites = [clean_text(website) for website in websites]
case_authorities = [clean_text(case) for case in case_authorities]

# Organize the data into a DataFrame
data = {
    'date_added': datetime.now().strftime('%Y-%m-%d'),
    'country': '',
    'source': 'This data was deleted for safety reasons',
    'name': brands,
    'url': websites,
    'status': '',
    'error': '',
    'notes': case_authorities,
    'date_added_to_website': dates
}

df = pd.DataFrame(data)

# Remove duplicate records based on 'name' and 'url' columns
df.drop_duplicates(subset=['name', 'url'], inplace=True)
today = date.today()

# Save the data to a CSV file
df.to_csv(f'Warning_List{today}.csv', index=False)

print(f"Data scraped, cleaned, and saved to ForexRev_Warning_List{today}.csv")
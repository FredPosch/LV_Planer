#all
import csv
import requests
from bs4 import BeautifulSoup

# Function to scrape the specified element from the URL
def scrape_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tr_element = soup.find('tr', {'id': 'ctl00_ctl00_ctl00_masterPlaceHolder_sitePlaceHolder_sitePlaceHolder_rowTermin', 'bgcolor': '#E4E4E4'})
            if tr_element:
                td_element = tr_element.find('td', style='width: 80%; padding-left: 2px;max-width: 500px;word-wrap:break-word;white-space:normal;')
                if td_element:
                    extracted_data = td_element.get_text(separator="\n")
                    return extracted_data.strip()
                else:
                    return "Inner TD Element not found"
            else:
                return "Outer TR Element not found"
        else:
            return f"Failed to fetch URL - Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request error: {str(e)}"

# Read the CSV file containing URLs and scrape all URLs
csv_file = 'extracted_urls.csv'  # Update with your file name
output_csv = 'allextracted_data.csv'  # Output file name
data = []  # List to store scraped data

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if exists
    for row in reader:
        url = row[0]  # Assuming URLs are in the first column
        result = scrape_content(url)
        data.append([url, result])

# Write the scraped data to a new CSV file
with open(output_csv, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL', 'Extracted Data'])  # Write header
    writer.writerows(data)

print(f"Data from all URLs has been scraped and saved to '{output_csv}'.")

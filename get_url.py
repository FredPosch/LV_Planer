import requests
from bs4 import BeautifulSoup
import csv

# Replace 'url_here' with the URL of the website you want to extract URLs from
url = 'https://portal.unilu.ch/stg/wf_ma_01/sem=HS23'  # Replace with your URL

# Send a GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all anchor tags (links) in the page
    links = soup.find_all('a', href=True)
    
    # Extract URLs starting with "../../details?code="
    extracted_urls = []
    for link in links:
        href = link['href']
        if href.startswith("../../details?code="):
            # Remove the initial "../../" from the URL
            cleaned_url = href.replace("../../", "")
            
            # Add "https://portal.unilu.ch/" to the cleaned URL
            full_url = f"https://portal.unilu.ch/{cleaned_url}"
            
            extracted_urls.append(full_url)
    
    # Create a CSV file and write the extracted URLs
    csv_filename = 'extracted_urls.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Extracted URLs'])
        for url in extracted_urls:
            csv_writer.writerow([url])
    
    print(f"Extracted URLs are saved in '{csv_filename}'")
else:
    print("Failed to retrieve the webpage")

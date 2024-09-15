import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL for the POST request
url = 'https://www.mse.mk/mk/stats/symbolhistory/TTK'

# Define custom date range and code
data = {
    'FromDate': '1.5.2024',
    'ToDate': '15.9.2024',
    'Code': 'TTK'  # Example selected value from the dropdown
}

# Make the POST request
response = requests.post(url, data=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Define headers based on the provided headers
    headers = [
        'Датум',
        'Цена на последна трансакција',
        'Мак.',
        'Мин.',
        'Просечна цена',
        '%пром.',
        'Количина',
        'Промет во БЕСТ во денари',
        'Вкупен промет во денари'
    ]
    
    # Find the table
    table = soup.find('table')  # Adjust selector if necessary
    
    if table:
        # Extract table rows
        rows = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                row_data = [cell.get_text(strip=True) for cell in cells]
                rows.append(row_data)
        
        # Create a DataFrame and write to CSV
        df = pd.DataFrame(rows, columns=headers)
        df.to_csv('filtered_output.csv', index=False)
        print("Filtered data successfully written to 'filtered_output.csv'.")
    else:
        print("No table found on the page.")
else:
    print("Failed to retrieve data. Status code:", response.status_code)

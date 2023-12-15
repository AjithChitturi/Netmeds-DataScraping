import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

url = 'https://www.netmeds.com/prescriptions'
data_list = []  # List to store dictionaries with disease and medicine information

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    products_div = soup.find('div', class_='prescriptions_products')

    if products_div:
        div_elements = products_div.find_all('div')

        for div in div_elements:
            a_elements = div.find_all('a')

            for a in a_elements:
                link_text = a.get_text()
                link_url = urljoin(url, a['href'])
                link_response = requests.get(link_url)

                if link_response.status_code == 200:
                    linked_soup = BeautifulSoup(link_response.content, 'html.parser')
                    products_div1 = linked_soup.find('div', class_='prescriptions_products')

                    if products_div1:
                        div_elements1 = products_div1.find_all('div')
                        link_texts1 = []  # List to store medicine names for each link

                        for div1 in div_elements1:
                            a_elements1 = div1.find_all('a')

                            for a1 in a_elements1:
                                link_text1 = a1.get_text()
                                link_texts1.append(link_text1)

                        data_list.append({'disease': link_text, 'Medicine': link_texts1})
                else:
                    print(f"Failed to retrieve linked page: {link_url}")

    else:
        print("No div with class 'products' found on the page.")
else:
    print(f"Failed to retrieve the page: {url}")

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data_list)

# Save the DataFrame to an Excel file
excel_filename = 'medicine_links1.xlsx'
df.to_excel(excel_filename, index=False)
print(f"Link texts saved to {excel_filename}")
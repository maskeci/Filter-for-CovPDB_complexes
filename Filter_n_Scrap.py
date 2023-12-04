import pandas as pd
from bs4 import BeautifulSoup
import requests
import Filter_by_Resolution

# STEP 1: All complexes will be filtered
all_proteins = Filter_by_Resolution.filter_complexes()

# STEP 2: CovPDB search, PDB id search term as name of complex as string 
def Find_url(complex_name: str):
    try:
        # URL of the page
        url = 'https://drug-discovery.vm.uni-freiburg.de/covpdb/search/search_type=by_pdb_idsearch_term=' + complex_name

        #  Fetch and parse the HTML content 
        response = requests.get(url)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the specific table
        all_tables = soup.find_all('table')
        for table in all_tables:
            thead = table.find('thead')
            if thead and 'Complex(es)' in thead.get_text(): # This is the table we are looking for
                target_table = table
                break

        # Extract URLs from the "SHOW" links
        show_urls = [link['href'] for link in target_table.select('tr.color1 a[href*="complex_card"]')]
        url = "https://drug-discovery.vm.uni-freiburg.de" + show_urls[0] 
        
        print('STEP 2 COMPLETED')
        return url
    except:
        print(f'STEP 2 ERROR: Certain PDB ID cannot be searched on CovPDB database.')
        return 

# STEP 3: Wildcard of the certain complex will be scraped 
def Data_Scraper(url : str):
    try:
        # Fetch and parse the HTML content 
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the specific table
        all_tables = soup.find_all('table')
        for table in all_tables:
            thead = table.find('thead')
            if thead and 'Covalent Mechanism' in thead.get_text(): # This is the table we are looking for

                target_table = table
                break
        
        # Converting as data frame
        rows = table.find_all('tr')
        headers = table.find_all('thead')[1].find_all('td')
        columns = [header.get_text(strip=True) for header in headers]

        data = [] # Empty list to store data

        # Iterate through rows and extract data
        for row in rows:
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            data.append(row_data)

        # Create a Pandas DataFrame
        df = pd.DataFrame(data, columns=columns)
        df = df.iloc[[0]]
        df = df.drop(columns='Warhead Structure', errors='ignore')

        print('STEP 3 COMPLETED')
        return df

    except:
        print('STEP 3 ERROR: Data cannot be scraped.')
        return


# STEP 4: Data will be concentrated as dataframe
dataset = pd.DataFrame()
not_collected = []

for protein in all_proteins:
    print(f'{protein} data is collecting')
    try:
        proteindata_url = Find_url(protein)
        data = Data_Scraper(proteindata_url)

        data = data.rename(index={0: protein})

        frames = [dataset,data]
        dataset = pd.concat(frames)

        print(f'Collected\n')
    except:
        not_collected.append(protein)
        print(f'{protein} data cannot be collected')

print(f'PROCESS FINISHED')
print('Not collected proteins: ', not_collected)

dataset.to_csv('Dataset.csv')
dataset.to_excel('Dataset.xlsx')
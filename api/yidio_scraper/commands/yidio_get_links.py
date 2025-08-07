import requests
import os

# Function to extract the movie links from Yidio
def get_movie_links(url, file_name="links.txt"):
    # Load existing links from file if available
    existing_links = set()
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            existing_links = set(line.strip() for line in f if line.strip())

    # Request new links from API
    params = {"type": "movie", "index": "0", "limit": "60000"}
    movie_links = set()

    try:
        with requests.get(url, params=params, timeout=10) as response:
            if response.status_code == 200:
                json_data = response.json()
                for item in json_data['response']:
                    movie_links.add(item['url'])  # avoid duplicates 
            else:
                print("Error fetching the page:", response.status_code)
    except requests.RequestException as e:
        print("An error occurred during the request:", e)

    # return only new links
    new_links = list(movie_links - existing_links)
    return new_links, movie_links.union(existing_links)

# Function to append only new links to file
def save_links_to_file(links, file_name):
    if not links:
        print("No new links to save.")
        return

    try:
        with open(file_name, 'w') as file:  # sobreescribe, no añade
            for link in sorted(links):  # orden opcional
                file.write(link + '\n')
        print(f"Saved {len(links)} total links to '{file_name}'.")
    except Exception as e:
        print("An error occurred while saving links to file:", e)

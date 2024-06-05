import requests

# Funct to extract the movie links
def get_movie_links(url):
    # Edit limit for more links (the limit is 50k)
    params = {"type": "movie", "index": "0", "limit": "1000"}
    movie_links = []

    try:
        with requests.get(url, params=params, timeout=10) as response:
            if response.status_code == 200:
                json_data = response.json()
                for item in json_data['response']:
                    movie_links.append(item['url'])
                return movie_links
            else:
                print("Error fetching the page:", response.status_code)
                return []
    except requests.RequestException as e:
        print("An error occurred during the request:", e)
        return []

# Save links in a txt file
def save_links_to_file(links, file_name):
    try:
        with open(file_name, 'w') as file:
            for link in links:
                file.write(link + '\n')
        print(f"Movie links have been saved to '{file_name}'.")
    except Exception as e:
        print("An error occurred while saving links to file:", e)


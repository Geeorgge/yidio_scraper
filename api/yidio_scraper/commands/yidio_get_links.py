import requests
import os

# Function to extract the movie links from Yidio
def get_movie_links(url, file_name="links.txt", min_links=63000):
    existing_links = set()

    # Read existing links from the file if it exists
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            existing_links = set(line.strip() for line in f if line.strip())

    # If the number of existing links is greater than or equal to min_links, skip fetching
    if len(existing_links) >= min_links:
        print(f"✅ Found {len(existing_links)} links in '{file_name}'. Skipping fetch.")
        # Return the links anyway, so parsing can continue
        return sorted(existing_links), existing_links

    print(f"⚠️ Only {len(existing_links)} links found. Fetching more...")

    # Download more links from Yidio
    params = {"type": "movie", "index": "0", "limit": str(min_links)}
    new_links = set()

    try:
        with requests.get(url, params=params, timeout=10) as response:
            if response.status_code == 200:
                json_data = response.json()
                for item in json_data['response']:
                    new_links.add(item['url'])
            else:
                print("❌ Error fetching links:", response.status_code)
    except requests.RequestException as e:
        print("❌ Request error:", e)

    combined_links = existing_links.union(new_links)

    # Save the combined links to the file
    if combined_links:
        with open(file_name, 'w') as file:
            for link in sorted(combined_links):
                file.write(link + '\n')
        print(f"✅ Saved {len(combined_links)} links to '{file_name}'.")

    return sorted(new_links if new_links else combined_links), combined_links

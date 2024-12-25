from bs4 import BeautifulSoup
import requests

def decode_url(url=None):
    
    
    # Fetch HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the page.")
        return
    
    # Parse HTML and extract text
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text(separator='\n').strip()
    
    # Extract relevant section after "y-coordinate"
    if "y-coordinate" not in content:
        print("Invalid content structure.")
        return
    data_section = content.split("y-coordinate", 1)[1].strip()
    
    # Parse data into triplets
    lines = data_section.splitlines()
    triplets = [lines[i:i+3] for i in range(0, len(lines), 3) if len(lines[i:i+3]) == 3]
    
    # Determine grid size
    max_x = max(int(triplet[0]) for triplet in triplets)
    max_y = max(int(triplet[2]) for triplet in triplets)
    
    # Create and populate the grid
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, char, y in triplets:
        grid[int(y)][int(x)] = char
    
    # Print the grid
    for row in grid:
        print("".join(row))

# Example URL
url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'

decode_url(url)
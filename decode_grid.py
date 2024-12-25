import requests
from bs4 import BeautifulSoup

def decode_grid(doc_url):
  response = requests.get(doc_url)
  soup = BeautifulSoup(response.content, 'html.parser')

  rows = soup.find_all('tr')

  grid_data = {}
  for row in rows[1:]:
    cells = row.find_all('td')
    char = cells[0].text
    x_coord = int(cells[0].text)
    y_coord = int(cells[2].text)
    grid_data[(x_coord, y_coord)] = char

  max_x = max(coord[0] for coord in grid_data.keys())
  max_y = max(coord[1] for coord in grid_data.keys())

  for y in range(max_y + 1):
    for x in range(max_x + 1):
      print(grid_data.get((x,y), ' '), end='')
    print()

doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
decode_grid(doc_url)
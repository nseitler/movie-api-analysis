import requests
import csv
import re
from keys import api_key

def fetch_movie_data(csv_file_path):
    base_url = "http://www.omdbapi.com/"
    movie_data = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            imdb_id = row['IMDB']
            full_url = f"{base_url}?apikey={api_key}&i={imdb_id}"
            response = requests.get(full_url)

            if response.status_code == 200:
                movie_info = process_movie_data(response.json())
                if movie_info:
                    movie_data.append(movie_info)
            else:
                print(f"Failed to fetch data for IMDb ID {'imbd_id'}")

    return movie_data

def process_movie_data(movie):
    try:
        # Extracting and converting data
        title = movie.get('Title', 'N/A')
        runtime = int(movie.get('Runtime', '0').split(' ')[0])  # '120 min' -> 120
        genre = movie.get('Genre', 'N/A')
        awards = movie.get('Awards', 'N/A')
        
        # Extracting wins and nominations from the awards string
        wins = sum(map(int, re.findall(r'(\d+) win', awards)))
        nominations = sum(map(int, re.findall(r'(\d+) nomination', awards)))
        
        # Box office value conversion to integer (e.g., '$123,456,789' -> 123456789)
        box_office = int(movie.get('BoxOffice', '$0').replace('$', '').replace(',', ''))

        return [title, runtime, genre, wins, nominations, box_office]
    except ValueError:
        # Handles cases where data conversion is not possible
        print(f"Error processing movie: {movie.get('Title', 'Unknown')}")
        return None

def save_to_csv(movie_data, output_file='movies.csv'):
    headers = ['Movie Title', 'Runtime', 'Genre', 'Award Wins', 'Award Nominations', 'Box Office']

    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(movie_data)
        
movie_data = fetch_movie_data('oscar_winners.csv')
save_to_csv(movie_data)
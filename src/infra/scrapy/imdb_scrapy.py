from domain.models.person import Person
from domain.models.rating import Rating
from domain.models.movie import Movie
from domain.models.genre import Genre
from dataclasses import dataclass
from bs4 import BeautifulSoup
from random import randint
from warnings import warn
from requests import get
from typing import List
from time import sleep
import numpy as np
import requests
import uuid
import re


@dataclass
class IMDBScrapy:

    def __post_init__(self, max_page: int = 5000):
        genres = [
             "adventure",
             "animation",
             "biography",
             "comedy",
             "crime",
             "drama",
             "family",
             "fantasy",
             "film-Noir",
             "history",
             "horror",
             "music",
             "musical",
             "mystery",
             "romance",
             "sci-fi",
             "sport",
             "thriller",
             "war",
             "western"
        ]

        self.urls = []
        pages = np.arange(1, max_page, 50)
        self.headers = {'Accept-Language': 'en-US,en;q=0.8'} 

        for genre in genres:
            for page in pages:
                url = "https://www.imdb.com/search/title?genres={}&start={}&explore=title_type,genres&title_type=movie&ref_=adv_prv"
                formated_url = url.format(genre, str(page))
                self.urls.append({
                    "url":formated_url,
                    "genre": genre,
                    "page": page
                    })
        
        self.count = -1
        self.movies = []
        self.have_movies = True
    
    def get_next_response(self):
        if self.count == len(self.urls):
            self.count = -1
            self.have_movies = False
        else:
            self.count += 1

        url = self.urls[self.count]

        print(f"""Genre: {url["genre"]}, Page: {url["page"]}""")
        response = get(url["url"], headers=self.headers)
        
        return response
    

    def get_movie(self, container) -> Movie:
        if container.find('div', class_ = 'ratings-metascore') is not None:
            film = {}
            film["title"] = container.h3.a.text

            year = container.h3.find('span', class_= 'lister-item-year text-muted unbold')
            film["year"] = re.sub('[^0-9]', '', year.text) if year else None

            rating = container.p.find('span', class_ = 'certificate')
            film["rating"] = rating.text if rating else None

            genre = container.p.find('span', class_ = 'genre')
            if genre:
                genres = genre.text.replace("\n", "").rstrip().split(',')
                film["genre"] = [g.strip() for g in genres]

            time = container.p.find('span', class_ = 'runtime')
            film["time"] = time.text.replace(" min", "") if time else None

            imdb = float(container.strong.text)
            film["imdb_ratings"] = imdb if imdb else None

            m_score = container.find('span', class_ = 'metascore')
            film["metascore"] = m_score.text if m_score else None

            description = container.find_all('p', class_ = 'text-muted', limit=2)
            if len(description) >=1:
                description = description[1].text.replace("\n", "")
            else:
                description = None
            film["description"] = description

            persons = container.find("div", class_ = "lister-item-content").find("p", class_ = "")
            directors = persons.text.split("|")[0]
            actors = persons.text.split("|")[1]
            film["director"] = directors.replace("\n", "").replace("Director:", "").replace("Directors:", "").strip().split(", ")

            film["actor"] = actors.replace("\n", "").replace("Star:", "").replace("Stars:", "").strip().split(", ")

            vote = container.find('span', attrs = {'name':'nv'})['data-value']
            film["votes"] = int(vote) if vote else None

            genres = []
            for genre in film["genre"]:
                genres.append(Genre(name=genre))

            actors = []
            for actor in film["actor"]:
                actors.append(Person(id=uuid.uuid4(), name=actor))
            
            directors = []
            for director in film["director"]:
                directors.append(Person(id=uuid.uuid4(), name=director))

            return Movie(
                id=uuid.uuid4(),
                type="movie",
                name= film["title"],
                description=film["description"],
                rating=Rating(
                    id=uuid.uuid4(),
                    rating=film["rating"],
                    votes=film["votes"],
                    metascore=film["metascore"],
                    imdb_ratings=film["imdb_ratings"]
                ),
                genre=genres,
                year=film["year"],
                duration=film["time"],
                actor=actors,
                director=directors,
            )
        return None
    
    def search_movies(self) -> List[Movie]:
        self.movies = []
        response = self.get_next_response()
        
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        else:
            page_html = BeautifulSoup(response.text, 'html.parser')
                
            movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
        
            for container in movie_containers:
                movie = self.get_movie(container)
                if movie:
                    self.movies.append(movie)
        
    
    def search_all(self) -> List[Movie]:
        try:
            self.search_movies()
            sleep(randint(2, 50))
        except:
            print("Excedeed limit")
            sleep(randint(100, 500))
        return self.movies
        
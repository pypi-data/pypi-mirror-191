import requests
from bs4 import BeautifulSoup
import re


class hunter():
    """
    # lyrics_Hunter - Ayush Lakra
    
    Class containing a function to scrape lyrics from lyrics.com
    
    """
    
    def scrape(song_name):
        
        # Original Query by User
        query = song_name
        
        # Replacing the empty space with %20 to make it searchable
        query = query.split(" ")
        query = "%20".join(query)
        
        # Generating a link
        link = f"https://www.lyrics.com/lyrics/{query}"
        
        # Putting a request
        req = requests.get(link)
        
        # Parsing HTML content using BeautifulSoup
        soup = BeautifulSoup(req.text, 'html.parser')
        
        # Parsing the first song link
        links = []
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        link = f"https://www.lyrics.com/{links[53]}"
        
        # New request
        req = requests.get(link)
        soup = BeautifulSoup(req.text,  'html.parser')
        
        # Extracting Lyrics
        try:
            lyrics = []
            for link in soup.find_all('pre'):
                lyrics.append(link.text)
            lyrics = "".join(lyrics)
        except:
            lyrics = 'Currently Not Available'
            
        # Extraing Other Info
        
        # Title
        title = soup.find('h1').text
        
        # Artist
        artist = soup.find('h3').text
        
        # Album Name
        try:
            x = []
            for link in soup.find_all('h3'):
                x.append(link.find('a'))
            for i in range(len(x)):
                if str(x[i]).__contains__('album'):
                    album = str(x[i])
            album = album.split('>')
            album = album[1][0:-3]
        except:
            album = None
        
        # Images
        try:
            try:
                song_art = soup.find(title=title).find('img').get('src')
            except:
                song_art = soup.find(title=title).get('src')
        except:
            song_art = None
        try:
            try:
                artist_art = soup.find(title=artist).find('img').get('src')
            except:
                artist_art = soup.find(title=artist).get('src')
        except:
            artist_art = None
        try:
            try:
                album_art = soup.find(title=album).find('img').get('src')
            except:
                album_art = soup.find(title=album).get('src')
        except:
            album_art = None


        # Return the following dictionary
        data = {
            'title': title,
            'artist': artist,
            'album': album,
            'lyrics': lyrics,
            'img': {
                'album': album_art,
                'artist': artist_art,
                'song': song_art
            }
        }
        
        return data
    
print(hunter.scrape('blank space'))

# Used for testing snippets of code when errors arise
from googleapiclient.discovery import build
from utils import YT_API_KEY
import urllib.request
import re
from bs4 import BeautifulSoup
import requests

def ExtractChannelID(youtubeURL): # Intakes Youtube URL, returns Channel ID or Username depending on the format to be digested later on
    patternOne = r'@([a-zA-Z0-9_-]+)'
    patternTwo = r'(channel|user)/([a-zA-Z0-9_-]+)'
    patternThree = r'youtube.com/([a-zA-Z0-9_-]+)'

    matchOne = re.search(patternOne, youtubeURL)
    matchTwo = re.search(patternTwo, youtubeURL)
    matchThree = re.search(patternThree, youtubeURL)

    if matchOne: # If it is patternOne (@Username), partial scrape job; Scrape for the channel ID using Beautifulsoup
        response = requests.get(youtubeURL)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            newURL = soup.find('link', rel='canonical')['href'] # This is the channel URL

            return ExtractChannelID(newURL)

        else:
            print('Invalid URL: Status Code:', response.status_code)

        #print(matchOne.group(1))
        #return matchOne.group(1)
    
    elif matchTwo:
        #print(matchTwo.group(2))
        return matchTwo.group(2)
    
    elif matchThree:
        #print(matchThree.group(1))
        return matchThree.group(1)
    else:
        return None
    

ExtractChannelID('https://www.youtube.com/@GianLecoMC')  
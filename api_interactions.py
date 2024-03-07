# All API interactions with Youtube and other platforms go through here
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from utils import YT_API_KEY
from pytube import YouTube
import requests
from pytube import YouTube
import re

"""
NOTES:
 - Fixed issue with YTChannelVideoIDCollection(), however, bug will arise if you input a channel name with 24 characters.
 - This is because the funciton will assume that it is a channel ID and will not check it accordingly, so it will not work.
 - Fix later!
"""
# Youtube API Interactions
youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

def YTVideoDownloadBackground(videoID): # Downloads a Youtube video from a non-copyright source; Background
    videoURL = f"https://www.youtube.com/watch?v={videoID}"
    youtube = YouTube(videoURL)
    youtube.streams.get_highest_resolution().download(output_path='C:\\Users\\13212\\Desktop\\Project Files\\ShortsAutomation\\RawVideoData', filename='background' + videoID + '.mp4')
    print('Download Complete')

def YTVideoDownloadContent(videoID): # Downloads a Youtube video from a non-copyright source; Content
    videoURL = f"https://www.youtube.com/watch?v={videoID}"
    youtube = YouTube(videoURL)
    youtube.streams.get_highest_resolution().download(output_path='C:\\Users\\13212\\Desktop\\Project Files\\ShortsAutomation\\RawVideoData', filename='content'+ videoID + '.mp4')
    print('Download Complete')

def YTChannelVideoIDCollection(channelURL): # Intakes Channel Username, returns list of IDs of all Youtube videos on the channel
    channelUsername = ExtractChannelID(channelURL) # Extract Channel ID from Username
    channelID = None
    
    if channelUsername is None:
        print('Invalid Channel Username: Issue with ExtractChannelID')
        return []
    
    # If the channelUsername is a channel ID, then we can skip the first part of the function
    if len(channelUsername) != 24: # If the channelUsername is not a channel ID;
        channelRequest = youtube.channels().list( # Request to Youtube API to get the channel ID
            part='id',
            forUsername = channelUsername
        )
        channelResponse = channelRequest.execute() 

        if 'items' not in channelResponse or not channelResponse['items']: # If the channel doesn't exist
            print('Channel not found')
            print('Channel Response:', channelResponse)  # Print channel response for debugging
            return []
    
        channelID = channelResponse['items'][0]['id']

    videoIDS = []
    nextPageToken = None

    while True:
        request = youtube.search().list( # Request to Youtube API
            part='snippet',
            channelId = channelID,
            maxResults = 50,
            pageToken = nextPageToken
        )
        response = request.execute() # Execute the request

        for item in response['items']: # Loop through the response and append video IDs to videoIDS
            if item['id']['kind'] == 'youtube#video':
                videoIDS.append(item['id']['videoId'])

        nextPageToken = response.get('nextPageToken') # Call for next toke
        if not nextPageToken: # break clause
            break

    return videoIDS       

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
    
    elif matchTwo:
        #print(matchTwo.group(2))
        return matchTwo.group(2)
    
    elif matchThree:
        #print(matchThree.group(1))
        return matchThree.group(1)
    else:
        return None

def YTPlaylistIDCollection(playlistURL): # Intakes Playlist URL, returns list of IDs that link to Youtube videos
    print('')   


print(YTChannelVideoIDCollection('https://www.youtube.com/@GianLecoMC')) 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
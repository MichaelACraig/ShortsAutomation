# All API interactions with Youtube and other platforms go through here
from googleapiclient.discovery import build
from utils import YT_API_KEY
import urllib.request
import re

# Youtube API Interactions
youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

def YTVideoDownload(videoID): # Downloads a Youtube video from a non-copyright source
    response = youtube.videos().list(
        part='snippet',
        id=videoID
    ).execute()

    videoURL = response['items'][0]['snippet']['thumbnails']['maxres']['url']

    urllib.request.urlretrieve(videoURL, 'video.mp4')

def YTChannelVideoIDCollection(channelURL): # Intakes Channel Username, returns list of IDs of all Youtube videos on the channel
    
    channelUsername = ExtractChannelID(channelURL) # Extract Channel ID from Username
    channelID = None
    
    if channelUsername is None:
        print('Invalid Channel Username')
        return []
    
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

    if matchOne:
        print(matchOne.group(1))
        return matchOne.group(1)
    
    elif matchTwo:
        print(matchTwo.group(2))
        return matchTwo.group(2)
    
    elif matchThree:
        print(matchThree.group(1))
        return matchThree.group(1)
    else:
        return None

def YTPlaylistIDCollection(playlistURL): # Intakes Playlist URL, returns list of IDs that link to Youtube videos
    print('')   
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
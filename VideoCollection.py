# Calls API Interactions and pulls video data into RawVideoData
from api_interactions import YTVideoDownload
import math

def MenuOne():
    print('1. Youtube\n2. Reddit\n3. Instagram\n4. Tiktok\n5. Facebook\n6. Twitter\n7. Twitch')
    while True:
        try:
            output = int(input("Enter the platform you're searching on:"))
            if 1 <= output <= 7:
                return output
            else:
                print('Invalid input. Please enter a number 1-7')
        except ValueError:
            print('Invalid input. Please enter a number 1-7')

def MenuYT():
    print('1. Download Video\n2. Download Videos from Channel\n3. Download Videos from Playlist')
    while True:
        try:
            output = int(input("Enter the action you want to perform:"))
            if 1 <= output <= 3:
                return output
            else:
                print('Invalid input. Please enter a number 1-3')
        except ValueError:
            print('Invalid input. Please enter a number 1-3')

choiceOne = MenuOne()

if choiceOne == 1:
    print('Youtube Selected')
    output = MenuYT()

    if output == 1:
        print('Download Video Selected')
        videoID = input('Enter the video ID: ')
        #YTVideoDownload(videoID)

    elif output == 2:
        print('Download Videos from Channel Selected')

    elif output == 3:
        print('Download Videos from Playlist Selected')        

elif choiceOne == 2:
    print('Reddit Selected')

elif choiceOne == 3:
    print('Instagram Selected')

elif choiceOne == 4:
    print('Tiktok Selected')

elif choiceOne == 5:
    print('Facebook Selected')

elif choiceOne == 6:
    print('Twitter Selected')

elif choiceOne == 7:
    print('Twitch Selected')    
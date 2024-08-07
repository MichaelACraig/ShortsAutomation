# Calls API Interactions and pulls video data into RawVideoData
from api_interactions import YTVideoDownloadBackground, YTVideoDownloadContent, YTChannelVideoIDCollection, ExtractChannelID

import math

'''
NOTES:
- Fix menus for bad inputs with Youtube

'''

def Preview():
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
    print('1. Download By Video\n2. Download Videos from Channel')
    while True:
        try:
            output = int(input("Enter the action you want to perform:"))
            if 1 <= output <= 2:
                return output
            else:
                print('Invalid input. Please enter a number 1-2')
        except ValueError:
            print('Invalid input. Please enter a number 1-2')

def mainMenu():
    choiceOne = Preview()

    if choiceOne == 1:
        print('Youtube Selected')
        output = MenuYT()

        if output == 1:
            print('Download By Video Selected')
            videoID = input('Enter the video ID: ')
            choiceTwoA = input('Is the video background or content? (b/c):')

            if choiceTwoA  == 'b':
                YTVideoDownloadBackground(videoID)

            elif choiceTwoA == 'c':
                YTVideoDownloadContent(videoID)    
            
            else:
                print('Invalid input. Please enter b or c')
        
        elif output == 2:
            print('Download Videos from Channel Selected')
            channelURL = input('Enter the channel URL: ')
            choiceTwoB = input('Is the video background or content? (b/c):')

            if choiceTwoB  == 'b':
                channelID = ExtractChannelID(channelURL)
                videos = YTChannelVideoIDCollection(channelURL)

                for YTVideo in videos:
                    YTVideoDownloadBackground(YTVideo)

            elif choiceTwoB == 'c':
                channelID = ExtractChannelID(channelURL)
                videos = YTChannelVideoIDCollection(channelURL)

                for YTVideo in videos:
                    YTVideoDownloadContent(YTVideo)

            else:
                print('Invalid input. Please enter b or c')              

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

mainMenu()            
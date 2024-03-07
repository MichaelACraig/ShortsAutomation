# Contains all of the code for editing the video
from moviepy.editor import *
from moviepy.video.fx.all import crop, resize, even_size
from utils import RAW_VIDEO_PATH, RAW_AUDIO_PATH

import speech_recognition as sr

# Libraries that might be needed; Not used currently
#import matplotlib.pyplot as plt
#import pygame


"""
NOTES:

Functions to Create:
BackgroundCrop(rawVideo): Crop background video to Shorts size; Returns a cropped video
ContentCrop(rawVideo): Crop content video to Shorts size; Returns a cropped video
TranscribeAudio(rawVideo): Creates a caption for the video inputted; Returns a text object
Overlay(BottomVideo, TopVideo): Overlay content video on top of background video; Returns a new video
AddCaption(caption): Creates a visual representation of the caption; Return a video overlay
CreateVideo(BackgroundVideo, ContentVideo): Creates a video from the background and content video; Returns a new video
CreateRandomVideo(BackgroundVideo, ContentVideo): Creates a random video from the background and content video; Returns a new video
"""

def BackgroundCrop(RawVideo): # Crops video to Shorts size, argument is rawVideo path
    name = RawVideo.split("\\")[-1]

    video = VideoFileClip(RawVideo)
    (w,h) = video.size
    croppedVideo = crop(video, width=656, height=5000, x_center=w/2, y_center=h/2)

    croppedVideo.write_videofile(RAW_VIDEO_PATH + "BCrop_" + name)

def ContentResize(RawVideo): # Reduces size of content to be overlayed properly, argument is rawVideo path
    name = RawVideo.split("\\")[-1]
    
    video = VideoFileClip(RawVideo)
    #(w,h) = video.size
    resizedVideo = resize(video, newsize=(500, 500)) # Fix resolution size to be more accurate for Shorts overlay
    resizeVideo = even_size(resizedVideo)

    resizedVideo.write_videofile(RAW_VIDEO_PATH + "Resized_" + name)

def Overlay(BottomLayerVid, TopLayerVid):
    background = VideoFileClip(BottomLayerVid)
    overlay = VideoFileClip(TopLayerVid)

    x = (background.size[0] - overlay.size[0]) / 2
    y = (background.size[1] - overlay.size[1]) / 2

    overlay = overlay.set_position((x, y)) # Centers the overlay to be in the center of the video

    final = CompositeVideoClip([background, overlay])

    final.write_videofile(RAW_VIDEO_PATH + "Overlayed.mp4")

def TranscribeAudio(RawVideo):
    name = RawVideo.split("\\")[-1]

    audio = AudioFileClip(RawVideo)
    audio.write_audiofile(RAW_AUDIO_PATH + name + "audio.wav")

    r = sr.Recognizer()

    with sr.AudioFile(RAW_AUDIO_PATH + name + "audio.wav") as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)

        return text

def AddCaption(RawVideo, CaptionText): # Needs some rework
    name = RawVideo.split("\\")[-1]

    video = VideoFileClip(RawVideo)

    caption = TextClip(CaptionText, fontsize=24, color='white', bg_color='black')

    caption = caption.set_position(('center', 'bottom')).set_duration(video.duration)

    finalVideo = CompositeVideoClip([video, caption])

    finalVideo.write_videofile(RAW_VIDEO_PATH + name + "Captioned.mp4")
    

def CreateVideo(BackgroundVideo, ContentVideo):
    pass

def CreateRandomVideo(BackgroundVideo, ContentVideo):
    pass

BackgroundCrop(RAW_VIDEO_PATH + "backgroundR0b-VFV8SJ8.mp4")
ContentResize(RAW_VIDEO_PATH + "contentyPM77NPZyJo.mp4")
Overlay(RAW_VIDEO_PATH + "BCrop_backgroundR0b-VFV8SJ8.mp4", RAW_VIDEO_PATH + "Resized_contentyPM77NPZyJo.mp4")
AddCaption(RAW_VIDEO_PATH + "Overlayed.mp4", TranscribeAudio(RAW_VIDEO_PATH + "Resized_contentyPM77NPZyJo.mp4"))

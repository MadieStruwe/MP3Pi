'''
MusicPlayer. py is where all the functitons for the music player are
the player will start on bootup if MusicPlayer.service is also used
pressing and realsing the button will skip to the next song
holding the button down will send a shutdown signal so the pi is shut 
down properly
'''


'''
import libraries
'''
import os
import pygame as pg
import RPi.GPIO as GPIO
from time import sleep
from aiy.board import Board, Led

#ignore the warnings
GPIO.setwarnings(False)
'''
set up GPIO for the button
'''
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN) #button
GPIO.setup(25, GPIO.OUT) #LED in button

'''
set function input values
'''
# optional volume 0 to 1.0
volume = 0.05
#initial starting place of the play list
i=0
#main directory we want to find music in
#this will change based on where the music is saved to 
MainDirect='/home/pi/Music'

'''
GetSongList function
input is the main directory we will start from
this function will go through the directory
and subdirectories and add all files to our
playlist
'''
def GetSongList(MainDirect):
    #create a list of the files and sub-directs
    ListOfFile = os.listdir(MainDirect)
    AllFiles = list()
    #iterate over the entries
    for entry in ListOfFile:
        #create the full path for sub-directs
        FullPath = os.path.join(MainDirect, entry)
        #if the full path is sub direct, get list of files
        if os.path.isdir(FullPath):
            AllFiles = AllFiles + GetSongList(FullPath)
        #otherwise, just add the file to the list
        else:
            AllFiles.append(FullPath)
    #sort the files alpha-numericly
    AllFiles.sort()
    #now going to remove the files that are not mp3s        
    for i,j in enumerate (AllFiles):
        if 'mp3' not in j:
            del AllFiles[i]
    return AllFiles

'''
ShutDown function
fucntion to send a shutdown signal
'''
def ShutDown():
    print ("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

'''
PlayMusic function
main function where we do things
inputs are the volume and initial starting place in songlist
we set up the mixer to play music,
then we begin to iterate through the list,
while doing this we check if the user pushes the button
    while the button is pushed, it lights up
    if they push the button, we want to skip to the next song
    if the button is being held down, we want to see if we should shut down
    if the button is not pushed, we will finish the current song
        and then move to the next song in out list
when we are through the list, the index will be set to 0 so
    we can repeat the play list
'''
#GPIO.add_event_detect(23, GPIO.FALLING, callback=myInterrupt, bouncetime=500)
def PlayMusic(volume, i):
    #set up a counter to detect if long button press
    counter = 0
    # set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 1     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    pg.mixer.music.set_volume(volume)
    #we're gunna itterate through the list and play the songs
    ListLength=len(SongList)
    #test print line
    #print ('length of list is ', ListLength)
    while i < ListLength:
        #load the current song
        pg.mixer.music.load(SongList[i])
        #print test
        print ("Now Playing - ", SongList[i])
        pg.mixer.music.play()
        #if the button is pushed, do stuff
        with Board() as board:
            while True:
                #if the button was pushed, skip to the next song
                if (GPIO.input(23) == False):
                    #print test
                    print ("The Button Was Pushed")
                    #counter for shutdown signal
                    counter += 1
                    #if the counter is above 20, send the shutdown signal
                    if counter > 20:
                        #print test
                        print ("I want to sleep")
                        sleep(0.5)
                        #call the shutdown function
                        ShutDown()
                    #light up and the button
                    GPIO.output(25, GPIO.HIGH)
                    sleep(0.25)
                    #if button is release, turn off the light
                    #and move to next song
                    if (GPIO.input(23) == True):
                        print ("The Button Was Released")
                        GPIO.output(25, GPIO.LOW)
                        #move the index up
                        i += 1
                        #if it can still play a song, do so
                        if i < ListLength:
                            #print test
                            print ("Playing Next Song")
                            PlayMusic(volume,i)
                        #if it will move 'outside' the song list,
                        #set it back to 0 and start it over
                        else :
                            #print test
                            print ("Restarting List")
                            i = 0
                            PlayMusic(volume,i)
            #if the song finished on its own, play the next song 
                elif pg.mixer.music.get_busy()==False:
                    #print test
                    print ("Song Ended")
                    i += 1
                    #print test
                    print ("Playing Next Song")
                    PlayMusic(volume,i)
                    #if it can still play a song, do so
                    if  i < ListLength:
                        #print test
                        print ("Playing Next Song")
                        PlayMusic(volume,i)
                    #if it will move 'outside' the song list,
                    #set it back to 0 and start it over
                    else :
                        #print test
                        print ("Restarting List")
                        i = 0
                        PlayMusic(volume,i)
                        
'''
run the functions
'''
#make a song list will all my files
GetSongList(MainDirect)
SongList = GetSongList(MainDirect)
#play music
PlayMusic(volume, i)
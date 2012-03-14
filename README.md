Pulseaudio Record Utility
=========================
Easily record audio and split it

Usecase
-------
Recording audiostreams with PulseAudio isn't very hard. This simple 
script is intended to help you setting up PulseAudio in a way, which
allows you to record only those audio streams you want to record.
So you can record the audio-output of your favorite MP3 streaming site
without recording the audio output of the game your are playing 
meanwhile. 

What does the script allow you to do?
-------------------------------------
 1. List audio streams
 2. List sinks
 3. Create new sinks
 4. Move audio streams to sinks
 5. Record audio sinks
 6. Split audio files with mp3split using CDDB, cue sheets or silence detection
 
Example session
---------------
List audio streams:
    ./pure-utility.py -i 
Output:
    Available sink inputs:
    
    Input ID | Sink ID |                 Sink Name                  |  Media Name   |   Application Name   
    ---------+---------+--------------------------------------------+---------------+--------------------
      472    |    0    | alsa_output.pci-0000_00_1b.0.analog-stereo | ALSA Playback | ALSA plug-in [chrome]


Create a new Sink:

    ./pure-utility.py -c record


Move audio stream to the new sink

    ./pure-utility.py -m 472 record


Write this sink's audio to a file (out.mp3):

    ./pure-utility.py -r record


Exit recording:

    Simply press CTRL+C 


Automatically cut the recorded audio file into pieces:

    ./pure-utility.py -d out.mp3 120 12
    
In this example the tool "mp3splt" will try to create 12 songs, each
at least 120 seconds long by detecting silence in between the songs

Run a CDDB search, select a album and cut the mp3 file corresponding to
these album infos:

    ./pure-utility.py --cddb out.mp3
    
"mp3splt" will interactivly ask your for search terms.

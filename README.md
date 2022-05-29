# MP3Pi
MP3 player designed to work from as Raspberry Pi and AIY Voice Hat

MP3Pi is a project I decided to do with an AIY Voice Kit. 
I got the kit because making my own alexa Google Assistant sounded fun, after puting it togethre
I didn't use it much. So i thought could use AIY Voice HAT accessory board, arcade button, and speaker to make an MP3 player.
The player is assembaled in a similar way following the instructions in the maker's guide
which can be found here https://aiyprojects.withgoogle.com/voice-v1/ I decided not to use the Voice HAT microphone board.

the MusicPlayer.service file makes the file run on boot so a monitor, mouse, and keyboard are not required

The MusicPlayer.py file is where i create a playlist,  iterate through it, and loop if at the end of the list.
A shutdown signal is sent if the button is held down after an alloted time so the system can be shut down
and unplugged safely.

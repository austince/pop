# pop
Simple Server / Simple Popcorn controller

Please please, do not steal our api keys. That would be _mega_ lame.

## Flow: 
- You watch Netflix, a [Chrome Extension](https://github.com/austince/netflixAndChill) sends this server running on a local raspi a requests to make popcorn.
- The raspi, connected via GPIO controlled relay, starts up a popcorn maker
- The popcorn maker pops directly into a receptical placed upon a [Roomba](http://giphy.com/gifs/cat-roomba-cqG5aFdTkk5ig)
- An Arduino, connected to the raspi via serial port, listens for the end of kernel popping as let's the popper know to STOP
- When popping is timed-out, or no more kernels are popping, the server contacts an Android phone connected via serial ports to the Roomba
- The Android controls the motors of the Roomba, guiding the popcorn to you, cleaning up what it (and you) spill along the way.

In summary: Netflix -> Chrome -> Raspi -> Popcorn Popper, Arduino -> Raspi -> Android -> Roomba -> You

_Simple, no?_


This was made for the Stevens Institute of Technology **IEEE** Home Hackathon  
1 weekend  
21 Nov - 23 Nov 2015
#### Second Prize  

## Team:  
[Austin Cawley-Edwards](https://github.com/austince)  
[Christopher Blackwood](https://github.com/cblackwo)  
[Jesse Stevens](https://github.com/jessedusty)  

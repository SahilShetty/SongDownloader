# Song Downloader
Automatically downloads inputed songs

These both are very slow and impractical (especially the Top100.py) and I made these to practise web scrapping

SongDownloader.py -

  inputs -

    1) path for where the songs will be stored

    2) song name

    3) author name (optional)
    
   outputs -
   
    1) an mp3 folder (if not previously there)
    
    2) an mp4 folder (if not previously there)
    
    3) an mp3 of the song
    
    4) an mp4 lyrical video of the song from youtube

Top100.py -

  inputs -

    1) path for where the songs will be stored

    2) the range of trending songs to be downloaded from billboards top 100 -
      
          a) this should be 2 numbers between 1 to 100 where the entirety of the range is downloaded
          
          b) the 2 numbers should be seperated by a colon then space
          
  outputs -
  
    same as SongDownloader.py

(made in python 2.7)

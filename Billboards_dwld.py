import moviepy.editor as mp
from requests import get
import os
from string import ascii_letters as al
from bs4 import BeautifulSoup as Bsoup
from pytube import YouTube


def main(names = [], bsoup1 = Bsoup(get('https://www.billboard.com/charts/hot-100').text, 'lxml'), titles2 = [], remove = [], count = 0):

    def loop1(name):

        for i in range(len(name) - 1):

            if name[i] == ' ': name[i] = '+'
            
            if name[i] not in al and name[i] != '+':
                
                del name[i]
                loop1(name)

        return name


    path1 = raw_input('Path of any folder: ')
    os.chdir(path1)
    
    try:
        
        os.mkdir('mp4')
        os.mkdir('mp3')

    except WindowsError: None
    
    amount = raw_input('Range of songs\nformat - starting song + colon and space + ending song\nexample n1: n2: ').split(': ')
    while (1 + int(amount[1]) - int(amount[0])) > 11:
        amount = raw_input('You can only download 10 songs at a time before getting dreops in quality (change ip after re-doing): ').split(': ')
    am0 = int(amount[0])
    am1 = int(amount[1])

    for i in bsoup1.findAll('h2', {'class': 'chart-row__song'}):

        count += 1
        
        if count >= int(amount[0]) and count <= int(amount[1]): names.append(str(i.string))
            
        else: continue

    for name in names:

        name_ = name
        print '\n' + name_, 'is downloading'
        
        name = list(name)
        name = loop1(name)
        if name[-1] not in al: del name[-1]
        name = ''.join(name)

        bsoup2 = Bsoup(get('https://www.youtube.com/results?search_query=' + name + '+lyrics').text, 'lxml')
        
        for lnk in bsoup2.findAll('a'):

            href = lnk.get('href')
            
            if '/watch?v=' in href:
                
                url = ('https://www.youtube.com' + href)
                break

        for vName in bsoup2.findAll('a', {'href': href}): titles = vName.get('title')
        titles1 = list(titles)

        for t in titles1:

            if t == '(' or t == ')' or t == ' ' or t == '-' or t == '&' or t in al: titles2.append(t)

        try: yt = YouTube(url)
        
        except:
            
            print 'Sorry, but those are all the songs I can download not.'
            print 'Please click "okay"'
            exit()
        
        stream = yt.streams.first()
        stream.download(path1 + '/mp4')

        titles2 = ''.join(titles2)
        path2 = path1 + '/mp4/' + titles2

        try:
            
            clip = mp.VideoFileClip(path2 + ".mp4")
            os.chdir(path1 + '/mp3')
            clip.audio.write_audiofile(path1 + '/mp3/' + name_ + ".mp3")

        except IOError: print 'Cannot download', "'" + name_ + "'"
        
        titles2 = []

    return 'COMPLETE'

print 'Use of VPN is manditory'
print main()

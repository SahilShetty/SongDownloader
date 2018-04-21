import moviepy.editor as mp
from requests import get
import os
from string import *
from bs4 import BeautifulSoup as Bsoup
from pytube import YouTube


def main(path1, amount, names = [], bsoup1 = Bsoup(get('https://www.billboard.com/charts/hot-100').text, 'lxml'), titles2 = [], remove = [], error = False):

    def searchUrl(name):

        for i in range(len(name) - 1):

            if name[i] == ' ': name[i] = '+'
            
            if name[i] not in ascii_letters and name[i] != '+':
                
                del name[i]
                searchUrl(name)

        return name


    def video(bsoup2):

        for lnk in bsoup2.findAll('a'):

            href = lnk.get('href')
            
            if '/watch?v=' in href:

                for vName in bsoup2.findAll('a', {'href': href}):

                    if vName.get('title') != None:

                        titles1 = list(vName.get('title'))

                        for letter in titles1:

                            if letter not in tuple(ascii_letters) + tuple(punctuation) + tuple(' '):

                                truth = False
                                break
                            
                            else: truth = True

                        if truth:

                            url = ('https://www.youtube.com' + href)
                            return (url, titles1)

                        
    os.chdir(path1)

    try:
        
        os.mkdir('mp4')
        os.mkdir('mp3')

    except WindowsError: None

    if amount == None:
        
        amount = raw_input('Range of songs\nformat - starting song + colon and space + ending song\nexample n1: n2: ').split(': ')
        
        while int(amount[0]) >= int(amount[1]) and int(amount[1]) >= 100: amount = raw_input('Enter valid values: ').split(': ')

    count = int(amount[0]) - 1

    for i in bsoup1.findAll('h2', {'class': 'chart-row__song'}):

        count += 1
        
        if count >= int(amount[0]) and count <= int(amount[1]): names.append(str(i.string))
            
        else: continue

    for name_ in names:

        print '\n' + "'"+ name_ + "'", 'is downloading'
        
        name = searchUrl(list(name_))
        if name[-1] not in ascii_letters: del name[-1]
        name = ''.join(name)

        bsoup2 = Bsoup(get('https://www.youtube.com/results?search_query=' + name + '+lyrics').text, 'lxml')
        (url, titles1) = video(bsoup2)
        
        for t in titles1:

            if t == '(' or t == ')' or t == ' ' or t == '-' or t == '&' or t in ascii_letters: titles2.append(t)

        try: yt = YouTube(url)
        
        except:
            
            print 'Sorry, but those are all the songs I can download not.'
            raise KeyboardInterrupt
        
        stream = yt.streams.first()
        
        try: stream.download(path1 + '\\mp4')
        
        except:

            print 'Restarting'
            main(path1, [str(count), amount[1]])

        titles2 = ''.join(titles2)
        path2 = path1 + '\\mp4\\' + titles2

        try:
            
            clip = mp.VideoFileClip(path2 + ".mp4")
            os.chdir(path1 + '\\mp3')
            clip.audio.write_audiofile(path1 + '\\mp3\\' + name_ + ".mp3")

        except IOError: error = True

        titles2 = []
        if not error: print "'" + name_ + "'", 'has downloaded'
        else: print 'Cannot download', "'" + name_ + "'"
        error = False


main(raw_input('Path: '), None)
print 'FINISHED'

import moviepy.editor as mp
from requests import get
import os
from string import *
from bs4 import BeautifulSoup as Bsoup
from pytube import YouTube


def main(path1, pre_dwded, amount = raw_input('Range of songs: ').split(': '), count = 0, names = [], filNames = [], titles2 = [], error = False
         bsoup1 = Bsoup(get('https://www.billboard.com/charts/hot-100').text, 'lxml')):

    def searchUrl(name):

        for lett in range(len(name) - 1):

            if name[lett] == ' ': name[lett] = '+'
            
            if name[lett] not in ascii_letters and name[lett] != '+':
                
                del name[lett]
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

    for h2 in bsoup1.findAll('h2', {'class': 'chart-row__song'}):

        count += 1
        
        if count >= int(amount[0]) and count <= int(amount[1]) and str(h2.string) + '\n' not in pre_dwded:

            names.append(str(h2.string))
            filNames.append(str(h2.string))

    for name_ in names:

        print  '\n' + name_

        print '\n' + "'" + name_ + "'", 'is downloading'
        
        name = searchUrl(list(name_))
        if name[-1] not in ascii_letters: del name[-1]
        name = ''.join(name)

        bsoup2 = Bsoup(get('https://www.youtube.com/results?search_query=' + name + '+lyrics').text, 'lxml')
        (url, titles1) = video(bsoup2)
        
        for t in titles1:

            if t == '(' or t == ')' or t == ' ' or t == '-' or t == '&' or t in ascii_letters: titles2.append(t)

        try: yt = YouTube(url)
        
        except:
            
            print 'Restart'
            
            for delete in filNames[filNames.index(name_): ]: filNames.remove(delete)
            return filNames
        
        stream = yt.streams.first()
        
        try: stream.download(path1 + '\\mp4')
        
        except:

            print 'Restart'

            for delete in filNames[filNames.index(name_): ]: fil.Names.remove(delete)
            return filNames

        titles2 = ''.join(titles2)
        path2 = path1 + '\\mp4\\' + titles2

        try:
            
            clip = mp.VideoFileClip(path2 + ".mp4")
            os.chdir(path1 + '\\mp3')
            clip.audio.write_audiofile(path1 + '\\mp3\\' + name_ + ".mp3")

        except IOError: error = True

        if not error: print "'" + name_ + "'", 'has downloaded'
        
        else:

            filNames.remove(name_)
            print 'Cannot download', "'" + name_ + "'"

        titles2 = []
        error = False

    return filNames


path = raw_input('Path: ')

openfil = lambda mode, path: open(path + '\\dwd.txt', mode)

try:

    fil = openfil('r', path)
    pre_dwded = fil.readlines()
    

except IOError:
    
    fil = openfil('w', path)
    pre_dwded = []

fil.close()

fil = openfil('a', path)
for already in main(path, pre_dwded): fil.write(already + '\n')
fil.close()

print 'FINISHED'

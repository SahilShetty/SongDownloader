import moviepy.editor as mp
from requests import get
import os
from string import *
from bs4 import BeautifulSoup as Bsoup
from pytube import YouTube


def spider(path1, amount, songno = 0, names = {}, bsoup1 = Bsoup(get('https://www.billboard.com/charts/hot-100').text, 'lxml'), titles2 = [], error = False):

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

                for findTitle in bsoup2.findAll('a', {'href': href}):

                    if findTitle.get('title') != None:

                        titles1 = list(findTitle.get('title'))

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

    if amount == None: amount = raw_input('Range of songs\nformat - starting song + colon and space + ending song\nexample n1: n2: ').split(': ')

    count = int(amount[0]) - 1

    fil = open(path1 + '\\dwd.txt', 'r')

    for i in bsoup1.findAll('h2', {'class': 'chart-row__song'}):

        count += 1
        
        if count >= int(amount[0]) and count <= int(amount[1]) and (str(i.string) + '\n') not in fil.readlines(): names[str(i.string)] = count

        else: continue

    dwded = names.keys()
    
    for name_ in names.keys():

        songno += 1
        print '\n' + 'Song', songno, 'is downloading'
        
        name = searchUrl(list(name_))
        if name[-1] not in ascii_letters: del name[-1]
        name = ''.join(name)

        bsoup2 = Bsoup(get('https://www.youtube.com/results?search_query=' + name + '+lyrics').text, 'lxml')
        (url, titles1) = video(bsoup2)
        
        for t in titles1:

            if t == '(' or t == ')' or t == ' ' or t == '-' or t == '&' or t in ascii_letters: titles2.append(t)

        yt = YouTube(url)
        stream = yt.streams.first()
        
        try: stream.download(path1 + '/mp4')
        
        except:

            print 'Restarting download'
            spider(path1, [names[name_], amount[1]])

        titles2 = ''.join(titles2)
        path2 = path1 + '/mp4/' + titles2

        try:
            
            clip = mp.VideoFileClip(path2 + ".mp4")
            os.chdir(path1 + '\\mp3')
            clip.audio.write_audiofile(path1 + '\\mp3\\' + name_ + ".mp3")

        except IOError:

            error = True
            dwded.remove(name_)

        if not error: print 'Song number', songno, 'has downloaded'
        else: print 'Cannot download song number', songno

        titles2 = []
        error = False

    return dwded


def main():

    user = raw_input('Path of any folder: ')

    try: fil = open(user + '\\dwd.txt', 'a')
    except IOError: fil = open(user + '\\dwd.txt', 'w')
    fil = open(user + '\\dwd.txt', 'a')
    
    run = spider(user, None)

    for check in run: fil.write(check + '\n')
    fil.close()

    print 'COMPLETE'
    
    
main()

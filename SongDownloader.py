import os

import moviepy.editor as mp

from pytube import YouTube

from requests import get

from bs4 import BeautifulSoup as Bsoup


def creatUrl(string):

	string = string.lower()

	string = string.split(' ')

	string = '+'.join(string)

	return string


path = raw_input('\n\n' + 'Path: ')

os.chdir(path)

try:

	os.mkdir('mp3')

	os.mkdir('mp4')

except WindowsError: pass

song = raw_input('Song name: ')

url = creatUrl(song)

author = creatUrl(raw_input('Author name (optional): '))

url = 'https://www.youtube.com/results?search_query=' + url + '+by+' + author + '+lyrics'

youtube = Bsoup(get(url).text, 'lxml') # html parser

for link in youtube.findAll('a'):

	if '/watch?v=' in link.get('href'):

		href = 'https://www.youtube.com' + link.get('href')

		break

mp4 = YouTube(href)

stream = mp4.streams.first()

stream.download(path + '\\mp4')

os.chdir(path + '\\mp4')

read = os.popen("dir").readlines()

del read[0: 7] # amount of excess data

file = read[0] # extra data like time still there

file = list(map(str, file))

del file[- 1]

del file[0: 36]

file = ''.join(file)

clip = mp.VideoFileClip(file)

os.chdir(path + '\\mp3')

clip.audio.write_audiofile(song + '.mp3')

os.remove(file)

from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import os
import sys

def download_files(x,n):
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    for i in range(n):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i]) 
        print("Songs are downloading "+str(i+1)+" .......")
        mp4files = yt.streams.filter(only_audio=True).first().download(filename='song-'+str(i)+'.mp3')

    print("Your Songs has been downloaded")
    print("Starting to create mashup.....")

def merge_sound(n,y):
    if os.path.isfile("song-0.mp3"):
        try:
            fin_sound = AudioSegment.from_file("song-0.mp3")[0:y*1000]
        except:
            fin_sound = AudioSegment.from_file("song-0.mp3",format="mp4")[0:y*1000]
    for i in range(1,n):
        aud_file = str(os.getcwd()) + "/song-"+str(i)+".mp3"
        try:
            f = AudioSegment.from_file(aud_file)
            fin_sound = fin_sound.append(f[0:y*1000],crossfade=1000)
        except:
            f = AudioSegment.from_file(aud_file,format="mp4")
            fin_sound = fin_sound.append(f[0:y*1000],crossfade=1000)
        
    return fin_sound

def main():
    if len(sys.argv) == 5:
        x = sys.argv[1]
        x = x.replace(' ','') + "songs"
        try:
            n = int(sys.argv[2])
            y = int(sys.argv[3])
        except:
            sys.exit("Wrong Parameters entered")
        output_name = sys.argv[4]
    else:
        sys.exit('Wrong number of arguments provided (pls provide 4)')

    download_files(x,n)
    fin_sound = merge_sound(n,y)

    fin_sound.export(output_name, format="mp3")
    print("Mashup has been created successfully...")

if __name__ == '__main__':
    main()
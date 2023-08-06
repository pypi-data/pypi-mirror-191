from pytube import YouTube
import pydub 
import urllib.request
import re
import os
import sys


def main():
    delete_after_use = True                              
    if len(sys.argv) == 5:
        x = sys.argv[1]
        x = x.replace(' ','') + "songs"
        try:
            n = int(sys.argv[2])
            y = int(sys.argv[3])
        except:
            sys.exit("Incorrect Parameters!!!")
        output_name = sys.argv[4]
    else:
        sys.exit('Insufficient arguments passed in CLI. Exiting!!!')

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                                                      
    for i in range(n):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i]) 
        print("File "+str(i+1)+" downloading...")
        mp4files = yt.streams.filter(only_audio=True).first().download(filename='audio_'+str(i)+'.mp3')

    print("All files are downloaded.\nNow creating the mashup...")

    if os.path.isfile(str(os.getcwd())+"\\audio_0.mp3"):
        pydub.AudioSegment.converter = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
        try:
            fin_sound = pydub.AudioSegment.from_file(
                str(os.getcwd())+"\\audio_0.mp3", format='mp3')[20000:(y*1000+20000)]
        except:
            fin_sound = pydub.AudioSegment.from_file(
                str(os.getcwd())+"\\audio_0.mp3", format='mp4')[20000:(y*1000+20000)]
        for i in range(1, n):
            aud_file = str(os.getcwd())+"\\audio_"+str(i)+".mp3"
            fin_sound = fin_sound.append(pydub.AudioSegment.from_file(aud_file)[20000:(y*1000+20000)], crossfade=1000)
  
    try:
        fin_sound.export(output_name, format="mp3")
        print("Mashup created successfuly as " + str(output_name))
    except:
        sys.exit("Error while saving the file. Try a differrent file name.")
        
    if delete_after_use:
        for i in range(n):
            os.remove("audio_"+str(i)+".mp3")


if __name__ == '__main__':
    main()
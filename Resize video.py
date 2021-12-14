import os, ffmpeg
import tkinter as tk
from tkinter.ttk import Label
from tkinter import *
from tkinter.ttk import *  
from tkinter import messagebox  
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.constants import CENTER, E, RIGHT, W
import os
from threading import *
import multiprocessing



def compress_video(video_full_path,output_file_name,target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path,cmd="FFmpeg\\bin\\ffprobe.exe")
    # Video duration, in s.
    duration = float(probe['format']['duration'])

    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run(cmd="FFmpeg\\bin\\ffmpeg.exe")
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run(cmd="FFmpeg\\bin\\ffmpeg.exe")


window = tk.Tk() 

height = 55
width = 600

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (width/2))
y_cordinate = int((screen_height/2) - (height/2))

window.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))


window.title("Resize and encode videos")


video_name = Label(window,text="Video name: ",font =("Courier", 14))
video_name.grid(row=0,column=0,padx=5)


video_text = Text(window,height=1,width=50)
video_text.grid(row=0,column=1)

def open():
    global src
    src =fd.askopenfilename()


  
def threading():
    # Call work function
    Thread(target=encode).start()
    


def encode():
    global file_name
    file_name =src 
    output="Output videos\\"+video_text.get("1.0",END).strip() + ".mp4"
    print(file_name)
    print(output)
    print(src)
    compress_video(file_name,output,52000)
    print(f"Completed{output}")




open_button = Button(window,text="..",width=3,command=open)
open_button.grid(row=0,column=2,padx=10)

encode_button = Button(window,text='Encode',command=threading)
encode_button.grid(row=1,column=0,columnspan=3)

window.mainloop()

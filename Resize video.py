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
import datetime
import time


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

height = 170
width = 560

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (width/2))
y_cordinate = int((screen_height/2) - (height/2))

window.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))


window.title("Resize and encode videos")


#widgets
part_code = Label(window,text="كود المنتج",font =("Courier", 14))
part_code.grid(row=0,column=1,padx=5)


operation_code = Label(window,text="كود العملية",font =("Courier", 14))
operation_code.grid(row=1,column=1,padx=5)


machine_code = Label(window,text="رقم الماكينة",font =("Courier", 14))
machine_code.grid(row=2,column=1,padx=5)


operation_no = Label(window,text="المصنع",font =("Courier", 14))
operation_no.grid(row=3,column=1,padx=5)

target_size = Label(window,text="حجم الفيديو",font =("Courier", 14))
target_size.grid(row=4,column=1,padx=5)

video_text1 = Text(window,height=1,width=50)
video_text1.grid(row=0,column=0,padx=5)


video_text2 = Text(window,height=1,width=50)
video_text2.grid(row=1,column=0,padx=5)


video_text3 = Text(window,height=1,width=50)
video_text3.grid(row=2,column=0,padx=5)


video_text4 = Text(window,height=1,width=50)
video_text4.grid(row=3,column=0,padx=5)


video_text5 = Text(window,height=1,width=50)
video_text5.grid(row=4,column=0,padx=5)




#functions
def open():
    global src
    src =fd.askopenfilename()



def threading():
    # Call work function
    Thread(target=encode).start()
    


def encode():
    global file_name
    file_name =src 
    #modified video time
    ct = time.ctime(os.path.getmtime(src))
    ct=str(ct)

    #output destination
    output="Output videos\\"+video_text1.get("1.0",END).strip()+ "-"+video_text2.get("1.0",END).strip()+"-"+video_text3.get("1.0",END).strip()+"-Factory:"+video_text4.get("1.0",END).strip()+"-"+ct+".mp4"
    output=output.replace(":","_")

    print(file_name)
    print("\n",output,"\n")
    print(src)
    
    compress_video(file_name,output,int(video_text5.get("1.0",END).strip())*1000)
    
    print(f"\n ------------------- Completed {output} -------------------------------")



w= Frame(window)
w.grid(row=5,column=0)

open_button = Button(w,text="Open video",command=open)
open_button.grid(row=0,column=0,padx=10,pady=10)

encode_button = Button(w,text='Run',command=threading)
encode_button.grid(row=0,column=1,padx=10,pady=10)

window.mainloop()

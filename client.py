import socket
from threading import Thread
import sys
from tkinter import *
from tkinter import ttk
import ftplib
from ftplib import FTP
import os
import time
import ntpath #This is used to extract filename from path

from tkinter import filedialog
from pathlib import Path


from playsound import playsound
import pygame
from pygame import mixer

name = None
listbox =  None
filePathLabel = None

IP_ADDRESS='127.0.0.1'
PORT=8000
SERVER=None
BUFFER_SIZE=4096
clients={}
song_selected=None
global song_counter
song_counter=0

def play():
    global song_selected
    song_selected=listbox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()
    if(song_selected != ""):
        infolabel.configure(text="Now Playing: " +song_selected)
    else:
        infolabel.configure(text="")

def stop():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()
    infolabel.configure(text="")

def resume():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()

def pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()

def browseFiles():
    global song_counter
    global listbox
    global filePathLabel

    try:
        filename=filedialog.askopenfilename()
        filePathLabel.configure(text=filename)
        HOSTNAME="127.0.0.1"
        USERNAME="lftpd"
        PASSWORD="lftpd"

        ftp_server=FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding="utf-8"
        ftp_server.cwd('shared_files')
        fname=ntpath.basename(filename)
        with open(filename,'rb') as file:
            ftp_server.storbinary(f"STOR {fname}",file)
        
        ftp_server.dir()
        ftp_server.quit()

        listbox.insert(song_counter,fname)
        song_counter=song_counter+1
    
    except FileNotFoundError:
        print("Cancel Button Pressed")

def download():
    #textarea.insert(END,"\n"+"\nPlease wait file is downloading...")
    #textarea.see("end")

    song_to_download=listbox.get(ANCHOR)
    infolabel.configure(text="Downloading "+song_to_download)

    HOSTNAME="127.0.0.1"
    USERNAME="lftpd"
    PASSWORD="lftpd"
    home=str(Path.home())
    download_path=home+"/Downloads"
    ftp_server=ftplib.FTP(HOSTNAME,USERNAME,PASSWORD)
    ftp_server.encoding='utf-8'
    ftp_server.cwd('shared_files')
    
    local_filename=os.path.join(download_path,song_to_download)
    file=open(local_filename,'wb')
    ftp_server.retrbinary('RETR '+song_to_download,file.write)
    ftp_server.dir()
    ftp_server.close()
    ftp_server.quit()

    infolabel.configure(text="Download Complete")
    time.sleep(1)
    if(song_selected != ""):
        infolabel.configure(text="Now Playing "+song_selected)
    else:
        infolabel.configure(text="")






def musicWindow():
    global song_counter
    global filePathLabel
    global listbox
    global infolabel

    window=Tk()
    window.title('Music Window')
    window.geometry("400x400")
    window.configure(bg='LightSkyBlue')

    selectlabel=Label(window,text="Select Song",bg='LightSkyBlue',font=("Calibri",10))
    selectlabel.place(x=2,y=1)

    listbox=Listbox(window,height=10,width=39,bg='LightSkyBlue',activestyle='dotbox',borderwidth=2,font=("Calibri",10))
    listbox.place(x=10,y=18)
    for file in os.listdir('shared_files'):
        filename=os.fsdecode(file)
        listbox.insert(song_counter,filename)
        song_counter=song_counter+1

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    play_but=Button(window,text="Play",width=10,bd=1,bg='SkyBlue',font=("Calibri",10),command=play)
    play_but.place(x=30,y=200)

    stop_but=Button(window,text="Stop",width=10,bd=1,bg='SkyBlue',font=("Calibri",10),command=stop)
    stop_but.place(x=200,y=200)

    upload_but=Button(window,text="Upload",width=10,bd=1,bg='SkyBlue',font=("Calibri",10),command=browseFiles)
    upload_but.place(x=30,y=250)

    download_but=Button(window,text="Download",width=10,bd=1,bg='SkyBlue',font=("Calibri",10))
    download_but.place(x=200,y=250)

    resume_but=Button(window,text="Resume",width=10,bd=1,bg='SkyBlue',font=("Calibri",10),command=resume)
    resume_but.place(x=30,y=300)

    pause_but=Button(window,text="Pause",width=10,bd=1,bg='SkyBlue',font=("Calibri",10),command=pause)
    pause_but.place(x=200,y=300)

    infolabel=Label(window,text="",fg="blue",font=("Calibri",10))
    infolabel.place(x=4,y=280)

    window.mainloop()

def setup():


    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

    musicWindow()
setup()



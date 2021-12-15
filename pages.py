import tkinter as tk
from speech_to_text import VoiceInput
from generate_speech import Response
from text_to_speech import SpeakerOutput
import threading as thrd
from PIL import ImageTk, Image
import pygame

class HomePage(tk.Frame):
    """HOME PAGE"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        pygame.mixer.init()
        pygame.mixer.music.load("media/pokemusic.mp3")
        pygame.mixer.music.play(loops=0)

        image1 = Image.open("media/original.png")
        test = ImageTk.PhotoImage(image1)

        self.label1 = tk.Label(image=test)
        self.label1.image = test
        self.label1.place(x=-0, y=0, relwidth=1, relheight=1)

        self.button = tk.Button(parent, bg="#8cfffb", text="   Enter", font=('Arial', 10, 'bold'), command=self.submit, width=10)
        self.button.pack()


    def submit(self):
        """Checks whether the user enters their name and saves their name as a global variable"""
        self.parent.show_frame(ChatBotPage)
        self.button.destroy()
        self.label1.destroy()
        pygame.mixer.music.pause()
        self.parent.geometry("400x640")

class ChatBotPage(tk.Frame):
    """CONVERSATION PAGE"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        image1 = Image.open("media/openpd.png")
        test = ImageTk.PhotoImage(image1)

        self.label1 = tk.Label(image=test)
        self.label1.image = test
        self.label1.place(x=0, y=0, relwidth=1, relheight=1)

        self.txt = tk.Text(parent, width=57, height=24)
        self.txt.pack()
        self.txt.configure(font=("Arial", 10, "bold"), background="#CCFFFF")

        self.listen = tk.Button(parent, bg="#8cfffb", text="Start", font=('Arial', 10, 'bold'),
                  command=self.thread, width=10)
        self.listen.pack()

    def thread(self):
        th=thrd.Thread(target=self.listening)
        th.start()

    def listening(self):
        
        #Voice Input
        self.listen.config(text="Listening...")
        aud_obj = VoiceInput()
        text = aud_obj.get_input()
        newline = "\n"
        #self.txt.insert(tk.END, f"{newline}You: {text}")

        #Response
        self.listen.config(text="Speaking...")
        res = Response()
        res = res.get_response(text.split()) #convert the text into an array
        self.txt.insert(tk.END, f"{newline}{newline}Answer: {res}")
        

        #Speaker Output
        speaker = SpeakerOutput()
        speaker.t_t_s(res)

        #Reset button
        self.listen.config(text="Start")

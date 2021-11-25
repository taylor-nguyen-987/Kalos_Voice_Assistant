import tkinter as tk
from tkhtmlview import HTMLLabel
from deepspeech_audio import Audio
import threading as thrd
from PIL import ImageTk, Image
import pygame

listening = False #Boolean variable for the bot to decide whether to listen or not

class HomePage(tk.Frame):
    """HOME PAGE"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        pygame.mixer.init()
        pygame.mixer.music.load("music/pokemusic.mp3")
        pygame.mixer.music.play(loops=0)

        image1 = Image.open("imgs/original.png")
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

        image1 = Image.open("imgs/openpd.png")
        test = ImageTk.PhotoImage(image1)

        self.label1 = tk.Label(image=test)
        self.label1.image = test
        self.label1.place(x=0, y=0, relwidth=1, relheight=1)

        self.txt = tk.Text(parent, width=57, height=24)
        self.txt.pack()
        self.txt.configure(font=("Arial", 10, "bold"), background="#CCFFFF")

        self.listen = tk.Button(parent, bg="#8cfffb", text="   Start", font=('Arial', 10, 'bold'),
                  command=self.thread, width=10)
        self.listen.pack()

    def thread(self):
        th=thrd.Thread(target=self.switch)
        th.start()

    def switch(self):
        """Makes the bot start listening and stops the bot from listening
        when button is clicked again"""
        global listening
        if listening is True: #turn off the bot
            listening = False
            self.listen.config(text="Start")
        else: #if it is not listening
            aud_obj = Audio()
            listening = True
            self.listen.config(text="   Stop")
            text = aud_obj.get_result()
            newline = "\n"
            self.txt.insert(tk.END, f"{newline}You: {text}")



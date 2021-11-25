import tkinter as tk
import pages

class App(tk.Tk):
    """MAIN APP"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        window = tk.Frame(self)

        window.pack(side="top", fill="both", expand=True)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)


        self.title("Kalosdex")
        self.geometry("400x500") #widthxheight
        photo = tk.PhotoImage(file="imgs/pokeball.png")
        self.iconphoto(False, photo)

        self.curr_frame = None
        self.show_frame(pages.HomePage)

    def show_frame(self, slide):
        new_frame = slide(self)
        if self.curr_frame is not None:
            self.curr_frame.destroy()
        self.curr_frame = new_frame
        self.curr_frame.pack(side="top", fill="both", expand=True)


def main():
    root = App()
    root.mainloop()

if __name__ == "__main__":
    main()

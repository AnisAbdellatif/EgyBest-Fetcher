# pre-defined
import tkinter as tk
import threading

# local
from utils.Internet import Connected
from utils.Fetcher import Fetcher
from components.entryComponent import Entry as entryComponent
from components.QualityElement import QualityComponent
from components.DialogBox import DialogBox


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("500x650")
        self.resizable(0, 0)
        # set Title
        self.title("EgyBest Fetcher")
        self.__Start()
        self.mainloop()

    def __Start(self):
        self.seriesVars = {
            "name": tk.StringVar(value=''),
            "season": tk.StringVar(value=''),
            "episode": tk.StringVar(value='')
        }

        self.movieVars = {
            "name": tk.StringVar(value=''),
            "year": tk.StringVar(value='')
        }

        # Navbar to switch between movies and series
        self.Navbar = tk.Frame(self)
        self.Navbar.pack()

        tk.Button(self.Navbar, text="Series", command=lambda: self.switchPage('series')).grid(row=0, column=0)
        tk.Button(self.Navbar, text="Movies", command=lambda: self.switchPage('movies')).grid(row=0, column=1)

        self.FrameEntries = tk.Frame(self)
        self.FrameEntries.pack()

        self.FrameSeries = tk.Frame(self.FrameEntries)
        self.FrameMovies = tk.Frame(self.FrameEntries)

        self.switchPage("series")

        self.seriesEntries = {
            "Serie Name:": self.seriesVars["name"],
            "Season:": self.seriesVars["season"],
            "Episode:": self.seriesVars["episode"],
        }

        self.moviesEntries = {
            "Movie Name:": self.movieVars["name"],
            "Year:": self.movieVars["year"],
        }

        # inputs
        for entryName, entryValue in self.seriesEntries.items():
            entryComponent(self.FrameSeries, [list(self.seriesEntries.keys()).index(entryName), entryName, entryValue])
        for entryName, entryValue in self.moviesEntries.items():
            entryComponent(self.FrameMovies, [list(self.moviesEntries.keys()).index(entryName), entryName, entryValue])

        # submit btn
        self.submitBtn = tk.Button(self, text="Submit", command=self.__SearchPressHandler, width=50, bg="blue",
                                   foreground="white")
        self.submitBtn.pack(pady=20)

        # results frame
        self.FrameResults = tk.Frame(
            self, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.FrameResults.pack(expand=True, fill=tk.BOTH, ipady=5)

        # credits
        credits = "Made with <3 by Anis Abdellatif @2020 ;)"
        tk.Label(self, text=credits).pack()

    def switchPage(self, switchto):
        if switchto == "series":
            self.FrameMovies.grid_forget()
            self.FrameSeries.grid()
            self.currentWindow = "series"
        else:
            self.FrameSeries.grid_forget()
            self.FrameMovies.grid()
            self.currentWindow = "movie"

    def __SearchPressHandler(self):
        for entry in eval(f"self.{self.currentWindow}Vars.values()"):
            if entry.get().strip() == "":
                return
        self.submitBtn["state"] = tk.DISABLED

        self.__ClearResults()

        if self.currentWindow == "series":
            params = [
                self.seriesVars["name"].get().replace(' ', '-'),
                self.seriesVars["season"].get(),
                self.seriesVars["episode"].get()
            ]
        else:
            params = [
                self.movieVars["name"].get().replace(' ', '-'),
                self.movieVars["year"].get()
            ]

        # state = Connected()
        if True:
            print("Connected to Internet!")
            thread = threading.Thread(target=lambda *params: self.__fetch(params), args=params)
            try:
                thread.start()
            except RuntimeError:
                thread.run()

        else:
            msg = "Not connected to the internet!"
            DialogBox(self.master, "Connectivity Error", msg)
            self.submitBtn["state"] = tk.NORMAL

    def __fetch(self, params):
        waitText = tk.Label(self.FrameResults, text=f"Wait for results!", font='Helvetica 18 bold')
        waitText.pack(pady=5)
        self.fetcher = Fetcher(self.currentWindow, params)
        (status, fullinfo, qualities) = self.fetcher.FetchQualities()
        waitText.destroy()
        if status:
            tk.Label(self.FrameResults, text=f"Results for: {fullinfo}", font='Helvetica 18 bold') \
                .pack(pady=5)
            for quality in qualities:
                QualityComponent(self.FrameResults, quality, self.fetcher)
            tk.Button(self.FrameResults, text="Clear", command=self.__ClearResults,
                      width=50, bg="red").pack(pady=(10, 0))

        else:
            msg = f"Error getting download link for {fullinfo} \n{qualities}"
            DialogBox(self.master, "Error", msg)
            self.fetcher.closeBrowser()

        self.submitBtn["state"] = tk.NORMAL

    def __ClearResults(self):
        if (hasattr(self, 'fetcher')) and (not (self.fetcher is None)):
            self.fetcher.closeBrowser()
            self.fetcher = None

        for widget in self.FrameResults.winfo_children():
            widget.destroy()


App()
exit()

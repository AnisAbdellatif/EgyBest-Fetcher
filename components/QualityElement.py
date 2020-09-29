import tkinter as tk
import subprocess
import os.path

from components.DialogBox import DialogBox

class QualityComponent():
    def __init__(self, master, quality, fetcher):
        self.master = master
        self.quality = quality
        self.fetcher = fetcher
        FrameQuality = tk.Frame(master, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        FrameQuality.pack(pady=5)
        FrameLabels = tk.Frame(FrameQuality)
        FrameLabels.grid(row=0, column=0)
        FrameButton = tk.Frame(FrameQuality)
        FrameButton.grid(row=0, column=1)

        tk.Label(FrameLabels, text = f"Quality: {quality[0]}").pack()
        tk.Label(FrameLabels, text = f"Resolution: {quality[1]}").pack()
        tk.Label(FrameLabels, text = f"Size: {quality[2]}").pack()

        tk.Button(FrameButton, text="Download", command=self.__pressHandler, bg="green").pack()

    def __pressHandler(self):
        [status, fullinfo, link] = self.fetcher.getDownloadLink(self.quality)
        if status:
            msg = f"Success, here is the download link for {fullinfo} \n\n{link}"
        else:
            msg = f"Error, cannot get download link for {fullinfo} \n"
        title = fullinfo
        downloadButton = {
            "title": "Download with idm",
            "command": lambda: self.__downloadWithIdm(link)
        }
        DialogBox(self.master, title, msg, copiable=link, otherBtns=[downloadButton])

    def __downloadWithIdm(self, link):
        idmpath = "C:/Program Files (x86)/Internet Download Manager/IDMan.exe"
        if not os.path.exists(idmpath):
            msg = "Sorry but I couldn't find IDM directory, send this error to developer for a solution!"
            return DialogBox(self.master, "IDM not Found", msg, copiable = msg[:40])
        subprocess.check_call(
            [idmpath,
             "/a", "/d", link]
        )
        DialogBox(self.master, "Done", "Added link to IDM Q")
        

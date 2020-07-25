#!/usr/bin/python3

import urllib.request
import requests
import shutil
import configparser
import io
import os
import sys
import subprocess

import AnimatedGif
import screeninfo
import threading
from tkinter import *
from tkinter import messagebox

global_ret_code = 0
wine_path = '/home/vitaly/.PlayOnLinux/wine/linux-amd64/4.16'
wine_prefix = '/home/vitaly/.PlayOnLinux/wineprefix/Fer.al'
feral_dir = "/home/vitaly/.PlayOnLinux/wineprefix/Fer.al/drive_c/Feral/build/"


def start_game():
    wine_env = os.environ.copy()
    wine_env['WINEDIR'] = wine_path
    wine_env['WINEPREFIX'] = wine_prefix
    wine_env['PATH'] = "%s/bin:%s/drive_c/windows:%s" % (wine_env['WINEDIR'], wine_env['WINEPREFIX'], wine_env['PATH'])
    if "LD_LIBRARY_PATH" in wine_env:
        wine_env['LD_LIBRARY_PATH'] = "%s/lib64:%s" % (wine_env['WINEDIR'], wine_env['LD_LIBRARY_PATH'])
    else:
        wine_env['LD_LIBRARY_PATH'] = "%s/lib64" % wine_env['WINEDIR']
    wine_env['WINEDLLPATH'] = "%s/lib64/wine" % wine_env['WINEDIR']
    wine_env['WINELOADER'] = "%s/bin/wine64" % wine_env['WINEDIR']
    wine_env['WINESERVER'] = "%s/bin/wine64" % wine_env['WINEDIR']

    subprocess.Popen([wine_env['WINELOADER'],
                      "%s/Fer.al.exe" % feral_dir],
                     env=wine_env,
                     cwd=feral_dir)

    # subprocess.call(["/usr/share/playonlinux/playonlinux", "--run", "Fer.al"])


class Worker(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        global global_ret_code
        config = configparser.ConfigParser()
        config['version'] = {'latestVersionEndpoint': "none"}
        config.read('config.ini')
        version_check_url = config['version']['latestVersionEndpoint']

        launcher = configparser.ConfigParser()
        launcher['version'] = {'currentVersion': 'none'}
        launcher.read('game.ini')
        current_game_ver = launcher['version']['currentVersion']

        if version_check_url == "none":
            global global_ret_code
            self.parent.hide_window()
            global_ret_code = 1
            messagebox.showerror("Error", "Missing version endpoint url in the config.ini!!!")
            self.parent.close_window()
            return

        print("Checking the latest version...")
        try:
            version_check = urllib.request.urlopen(version_check_url)
            version_check_raw = version_check.read()
            version_check_data = "[root]\n" + version_check_raw.decode('utf-8')

            config = configparser.ConfigParser(allow_no_value=True)
            config.read_file(io.StringIO(version_check_data))

            latest_game_ver = config["root"]["ApplicationVersion"]
        except OSError as e:
            global_ret_code = 1
            self.parent.hide_window()
            messagebox.showerror("Fatal error",
                                 "Can't start a game!\n"
                                 "Error has occurred while update checking: %s" % e.reason)
            self.parent.close_window()
            return

        if os.path.isdir("build") and latest_game_ver == current_game_ver:
            print("Game is up to date!")
            global_ret_code = 0
            self.parent.hide_window()
            self.parent.close_window()
            return

        print("New version found: %s" % latest_game_ver)
        print("-----------------")
        print("Downloading an update...")

        download_package_url = config["root"]["ApplicationDownloadUrl"]

        file_name = "game_build.7z"

        if os.path.exists(file_name):
            os.remove(file_name)

        try:
            with open(file_name, "wb") as f:
                print("Downloading %s" % file_name)
                response = requests.get(download_package_url, stream=True)
                total_length = response.headers.get('content-length')

                self.parent.show_progress()

                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(100 * dl / total_length)
                        self.parent.set_progress(done)
                        # sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                        # sys.stdout.flush()
        except OSError as e:
            global_ret_code = 2
            self.parent.hide_window()
            messagebox.showerror("Fatal error",
                                 "Can't start a game!\n"
                                 "Error has occurred while downloading an update: %s" % e.reason)
            self.parent.close_window()
            return

        self.parent.hide_progress()

        if os.path.isdir("build"):
            os.rename("build", "build-old")

        print("Extracting...")
        os.system('7z x %s' % file_name)

        launcher['version']['currentVersion'] = latest_game_ver
        with open('game.ini', 'w') as configfile:
            launcher.write(configfile)

        print("Removing backups...")
        shutil.rmtree('build-old', ignore_errors=True)
        if os.path.exists(file_name):
            os.remove(file_name)

        print("-----------------")
        print("Update complete!")
        self.parent.hide_window()
        self.parent.close_window()


class App:
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(1)
        self.frame = Frame(self.root, width=501, height=496, borderwidth=0, relief=SOLID)
        self.frame.pack_propagate(False)
        self.frame.pack()

        self.label = Label(self.frame)
        self.label.place(x=-2, y=-2)

        # self.bQuit = Button(self.frame, text="X", command=self.root.quit)
        # self.bQuit.place(x=470, y=0)

        # (tkinter.parent, filename, delay between frames)
        self.lbl_with_my_gif = AnimatedGif.AnimatedGif(self.label, 'installer.gif', 0.06)
        self.lbl_with_my_gif.pack()  # Packing the label with the animated gif (grid works just as well)
        self.lbl_with_my_gif.start()  # Shows gif at first frame and we are ready to go

        self.progress_label = Label(self.frame, text="0%", bg="black", fg="#fff", font=("Tiki Island", 10))
        # self.show_progress()

        m = screeninfo.get_monitors()

        x = (m[0].width / 2) - (501 / 2)
        y = (m[0].height / 2) - (496 / 2)

        self.root.geometry("+%d+%d" % (x, y))

        self.worker = Worker(self)

    def start_work(self):
        self.worker.start()

    def show_progress(self):
        self.progress_label.place(x=445, y=460)

    def hide_progress(self):
        self.progress_label.place_forget()

    def set_progress(self, percent):
        self.progress_label['text'] = "%d%%" % percent

    def hide_window(self):
        # self.lbl_with_my_gif.stop()
        self.root.withdraw()

    def close_window(self):
        self.root.quit()


app = App()
app.start_work()
app.root.mainloop()

if global_ret_code == 0:
    start_game()

exit(global_ret_code)
